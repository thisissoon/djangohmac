from functools import wraps

from .sign import HmacException, shmac


def auth(only=None):
    """ Route decorator. Validates an incoming request can access the
    route function.

    Keyword Args:
        only (list): Optional list of clients that can access the view

    .. sourcecode:: python

        class SignedView(View):

            @decorators.auth()
            def get(self, request):
                return HttpResponse("For all services")

            @decorators.auth(only=['serviceA'])
            def post(self, request):
                return HttpResponse("Only for service A")

    """

    def decorator(route):
        @wraps(route)
        def _wrapped_view(view, request, *args, **kwargs):
            try:
                shmac.validate_signature(request, only)
            except HmacException:
                shmac.abort()
            return route(view, request, *args, **kwargs)
        return _wrapped_view
    return decorator
