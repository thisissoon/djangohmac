Instalation
===========

Install package:

.. code-block:: python

    pip install djangohmac


Middleware
----------

To secure all your app with HMAC you can use a middleware.

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        # ...
        'djangohmac.middleware.GlobalHmacMiddleware',
    )


If your application is called by multiple services and each has different secret keys you should use `djangohmac.middleware.GlobalHmacMiddleware` instead.

.. note:: Middleware is applied on all views except the admin!


Decorators
----------

You can specify views which are protected by HMAC by using decorators. You can also pass list of services which have access to the view. If the list is not given all services defined in settings have access.


.. sourcecode:: python

    class SignedView(View):

        @decorators.auth()
        def get(self, request):
            return HttpResponse("For all services")

        @decorators.auth(only=['serviceA'])
        def post(self, request):
            return HttpResponse("Only for service A")

Settings
--------

Single key:
~~~~~~~~~~~

.. sourcecode:: python

    HMAC_SECRET = 'HMAC_SECRET'


Multiple keys:
~~~~~~~~~~~~~~

.. sourcecode:: python

    HMAC_SECRETS = {
        'serviceA': 'HMAC_SERVICE_A_SECRET',
        'serviceB': 'HMAC_SERVICE_B_SECRET'
    }

Other settings:
~~~~~~~~~~~~~~~

    - HMAC_HEADER: HTTP header where signature is stored (Default: Signature)
    - HMAC_DIGESTMOD: Digest mod (Default: hashlib.sha256)
    - HMAC_DISABLE: Disable or enable HMAC True/False (Default: Enabled)
