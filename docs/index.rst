.. Django HMAC documentation master file, created by
   sphinx-quickstart on Wed Oct 14 17:03:36 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django HMAC's documentation!
=======================================

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


Contents:
~~~~~~~~~

.. toctree::
   :maxdepth: 2

   instalation
   examples
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
