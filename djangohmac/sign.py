# Standard Libs
import base64
import binascii
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


class UnknownKeyName(HmacException):
    pass


def encode_string(value):
    return value.encode('utf-8') if isinstance(value, six.text_type) else value


def decode_string(value):
    return value if isinstance(value, six.string_types) else value.decode('utf-8')


class Hmac(object):

    def __init__(self):
        self.header = getattr(settings, 'HMAC_HEADER', 'Signature')
        self.digestmod = getattr(settings, 'HMAC_DIGESTMOD', hashlib.sha256)
        self.hmac_disarm = getattr(settings, 'HMAC_DISABLE', False)
        self.hmac_keys = getattr(settings, 'HMAC_SECRETS', {})

    @property
    def hmac_key(self):
        return six.b(settings.HMAC_SECRET)

    def get_signature(self, request):
        try:
            return request.META['HTTP_{}'.format(self.header.upper())]
        except KeyError:
            raise SecretKeyIsNotSet()

    def _hmac_factory(self, data, key=None, digestmod=None):
        key = six.b(key) if key else self.hmac_key
        return hmac.new(key, data, digestmod=self.digestmod)

    def make_hmac(self, data='', key=None):
        ''' Generates HMAC key
        Arguments:
            data (str): HMAC message
            key (str): secret key of another app
        '''
        hmac_token_server = self._hmac_factory(encode_string(data), key).digest()
        hmac_token_server = base64.b64encode(hmac_token_server)
        return hmac_token_server

    def make_hmac_for(self, name, data=''):
        ''' Generates HMAC key for named key
        Arguments:
            name (str): key name from HMAC_SECRETS dict
            data (str): HMAC message
        '''
        try:
            key = self.hmac_keys[name]
        except KeyError:
            raise UnknownKeyName()
        token = base64.b64encode(six.b(
            '{0}:{1}'.format(name, decode_string(self.make_hmac(data, key)))
        ))
        return token

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

    def _parse_multiple_signature(self, signature):
        try:
            return decode_string(
                base64.b64decode(decode_string(signature))
            ).split(':')
        except (TypeError, binascii.Error):
            raise InvalidSignature()

    def validate_multiple_signatures(self, request):
        if self.hmac_disarm:
            return True
        signature = self.get_signature(request)
        key_name, hmac_token_client = self._parse_multiple_signature(signature)
        hmac_token_server = self.make_hmac_for(key_name, request.body)
        if signature != hmac_token_server:
            raise InvalidSignature('Signatures are different: {0} {1}'.format(
                signature, hmac_token_server
            ))
        return True


shmac = Hmac()
