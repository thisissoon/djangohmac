from .sign import HmacException, shmac


class HmacMiddleware(object):
    """ Uses global signature `HMAC_SECRET` defined in settings
    """
    def process_request(self, request):
        try:
            shmac.validate_signature(request)
        except HmacException:
            shmac.abort()
