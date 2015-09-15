# Third Party Libs
from django.core.exceptions import PermissionDenied

from .sign import HmacException, shmac


class GlobalHmacMiddleware(object):
    ''' Uses global signature `HMAC_SECRET` defined in settings
    '''
    def process_request(self, request):
        try:
            shmac.validate_signature(request)
        except HmacException:
            raise PermissionDenied()


class MultipleHmacMiddleware(object):
    ''' Uses multiple signatures defined in `HMAC_SECRETS` in settings
    '''

    def process_request(self, request):
        try:
            shmac.validate_multiple_signatures(request)
        except HmacException:
            raise PermissionDenied()
