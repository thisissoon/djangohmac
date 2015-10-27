# Standard Libs
import base64
import binascii
import hashlib
import hmac

# Third Party Libs
import six
from django.conf import settings
from django.core.exceptions import PermissionDenied


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
        self.hmac_keys = getattr(settings, 'HMAC_SECRETS', {})

    @property
    def hmac_disarm(self):
        if hasattr(settings, 'HMAC_DISABLE'):
            return settings.HMAC_DISABLE
        return False

    @property
    def hmac_key(self):
        return six.b(settings.HMAC_SECRET)

    def get_signature(self, request):
        """ Get signature from djagno requests

        Arguments:
            request: Django request

        Returns:
            string: HMAC signature

        Raises:
            SecretKeyIsNotSet
        """

        try:
            return request.META['HTTP_{}'.format(self.header.upper())]
        except KeyError:
            raise SecretKeyIsNotSet()

    def _hmac_factory(self, data, key=None, digestmod=None):
        key = six.b(key) if key else self.hmac_key
        return hmac.new(key, data, digestmod=self.digestmod)

    def make_hmac(self, data='', key=None):
        """ Generates HMAC key

        Arguments:
            data (str): HMAC message
            key (str): secret key of another app
        """
        hmac_token_server = self._hmac_factory(encode_string(data), key).digest()
        hmac_token_server = base64.b64encode(hmac_token_server)
        return hmac_token_server

    def make_hmac_for(self, name, data=''):
        """ Generates HMAC key for named key

        Arguments:
            name (str): key name from HMAC_SECRETS dict
            data (str): HMAC message

        Raises:
            UnknownKeyName
        """
        try:
            key = self.hmac_keys[name]
        except KeyError:
            raise UnknownKeyName()
        token = base64.b64encode(six.b(
            '{0}:{1}'.format(name, decode_string(self.make_hmac(data, key)))
        ))
        return token

    def _parse_signature(self, signature):
        """ Split signature to user name and signature

        Arguments:
            signature (string): Signature genrated by `make_hmac_for`

        Returns:
            tuple of service name and signature
        """
        try:
            return decode_string(
                base64.b64decode(decode_string(signature))
            ).split(':')
        except (TypeError, binascii.Error):
            raise InvalidSignature()

    def validate_signature(self, request, only=None):
        """ Validate signate in given request.

        Arguments:
            request: Django request
            only: list of keys from HMAC_SECRETS to restrict signatures

        Returns:
            boolean: True when signature is valid otherwice False

        Raises:
            InvalidSignature
            SecretKeyIsNotSet
        """
        if self.hmac_disarm:
            return True
        try:
            signature = self.get_signature(request)
            key_name, hmac_token_client = self._parse_signature(signature)
            if only and key_name not in only:
                raise InvalidSignature('This view is only for {}'.format(only))
            return self.validate_multiple_signatures(key_name, signature, request)
        except ValueError:
            return self.validate_single_signature(request)

    def validate_single_signature(self, request):
        """ Validate signature from djagno request

        Arguments:
            request (request): Django request class

        Returns:
            boolen

        Raises:
            InvalidSignature
        """
        hmac_token_client = self.get_signature(request)
        hmac_token_server = self.make_hmac(request.body)
        if hmac_token_client != hmac_token_server:
            raise InvalidSignature('Signatures are different: {0} {1}'.format(
                hmac_token_client, hmac_token_server
            ))
        return True

    def validate_multiple_signatures(self, key_name, signature, request):
        """ Validate signature from djagno request. But it takes key from
        `HMAC_SECRETS` list

        Arguments:
            request (request): Django request class
            only (list): Restricted only for this list of service

        Returns:
            boolen

        Raises:
            InvalidSignature
        """
        hmac_token_server = self.make_hmac_for(key_name, request.body)
        if signature != hmac_token_server:
            raise InvalidSignature('Signatures are different: {0} {1}'.format(
                signature, hmac_token_server
            ))
        return True

    def abort(self):
        """ Called when validation failed.

        Raises:
            PermissionDenied()
        """
        raise PermissionDenied()


shmac = Hmac()
