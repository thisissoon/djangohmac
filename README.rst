Django-HMAC
==========

|circle| |downloads| |version| |license| |docs|

This module provides a middleware for HMAC signature Django views. It's simply
designed to check that a client is entitled to access routes, based on the fact
that it must possess a copy of the secret key.

Key features:
~~~~~~~~~~~~~
- HMAC Middleware
- HMAC View decorators
- Multiple keys for more services
- Service restricted access

Small example
~~~~~~~~~~~~~

.. sourcecode:: python

    class SignedView(View):

        @decorators.auth
        def get(self, request):
            return HttpResponse("for all services")

        @decorators.auth(only=['userservice'])
        def post(self, request):
            return HttpResponse("Only for user service")


Dev
---

To run all tests

.. sourcecode::

    docker run -it -v $PWD:/src -w /src ikalnitsky/pythonista tox


.. |circle| image:: https://img.shields.io/circleci/project/thisissoon/djangohmac.svg
    :target: https://circleci.com/gh/thisissoon/djangohmac

.. |downloads| image:: http://img.shields.io/pypi/dm/djangohmac.svg
    :target: https://pypi.python.org/pypi/djangohmac

.. |version| image:: http://img.shields.io/pypi/v/djangohmac.svg
    :target: https://pypi.python.org/pypi/djangohmac

.. |license| image:: http://img.shields.io/pypi/l/djangohmac.svg
    :target: https://pypi.python.org/pypi/djangohmac

.. |docs| image:: https://readthedocs.org/projects/djangohmac/badge/?version=latest
    :target: http://djangohmac.readthedocs.org/en/latest/?badge=latest
