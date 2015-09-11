# Third Party Libs
from django.core.exceptions import PermissionDenied

# First Party Libs
from .sign import HmacException, shmac


class HmacMiddleware(object):

    def process_request(self, request):
        try:
            shmac.validate_signature(request)
        except HmacException:
            raise PermissionDenied()
