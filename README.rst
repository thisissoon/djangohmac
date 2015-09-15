Django-HMAC
==========

|circle| |downloads| |version| |license|

This module provides a middleware for HMAC signature Django views. It's simply
designed to check that a client is entitled to access routes, based on the fact
that it must possess a copy of the secret key.

The app can use neither single secret key which is used in every request or multiple
secret keys.

Usage
-----

settings.py
~~~~~~~~~~~

.. sourcecode:: python

    MIDDLEWARE_CLASSES = (
        # ...
        'djangohmac.middleware.GlobalHmacMiddleware',
        # or 'djangohmac.middleware.MultipleHmacMiddleware'
    )

    HMAC_SECRET = 'HMAC_SECRET'  # for global HMAC middleware
    # HMAC_SECRETS = {  # for multiple HMAC middleware
    #    'service': 'HMAC_SECRET'
    # }

Client
~~~~~~

.. sourcecode:: python

    from djangohmac.sign import shmac

    sig = shmac.make_hmac()  # generate signature
    response = requests.get(
        '/hmac_auth_view',
        headers={hmac.header: sig}
    )

    # or

    sig = shmac.make_hmac_for('service')  # generate signature for multiple HMAC
    response = requests.get(
        '/hmac_auth_view',
        headers={hmac.header: sig}
    )

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
