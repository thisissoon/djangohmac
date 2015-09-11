# Standard Libs
import base64
import hashlib
import hmac

# Third Party Libs
import six
from django.conf import settings


class HmacException(Exception):
    pass


class SecretKeyIsNotSet(HmacException):
    pass


class InvalidSignature(HmacException):
    pass


def encode_string(value):
    return value.encode('utf-8') if isinstance(value, six.text_type) else value


class Hmac(object):

    def __init__(self):
        self.hmac_key = six.b(settings.HMAC_SECRET)
        self.header = getattr(settings, 'HMAC_HEADER', 'Signature')
        self.digestmod = getattr(settings, 'HMAC_DIGESTMOD', hashlib.sha256)
        self.hmac_disarm = getattr(settings, 'HMAC_DISABLE', False)

    def get_signature(self, request):
        try:
            return request.META[self.header]
        except KeyError:
            raise SecretKeyIsNotSet()

    def _hmac_factory(self, data, digestmod=None):
        return hmac.new(self.hmac_key, data, digestmod=self.digestmod)

    def make_hmac(self, data=''):
        hmac_token_server = self._hmac_factory(encode_string(data)).digest()
        hmac_token_server = base64.urlsafe_b64encode(hmac_token_server)
        return hmac_token_server

    def validate_signature(self, request):
        if self.hmac_disarm:
            return True
        hmac_token_client = self.get_signature(request)
        hmac_token_server = self.make_hmac(request.body)
        if hmac_token_client != hmac_token_server:
            raise InvalidSignature('Signatures are different: {0} {1}'.format(
                hmac_token_client, hmac_token_server
            ))
        return True


shmac = Hmac()
