Examples
========

The signature is build from a secret key and a request body if exists.


Python
-------

To send valid HMAC signature to a view you can use `shmac.make_hmac()`

.. sourcecode:: python

    from djangohmac.sign import shmac

    sig = shmac.make_hmac()  # generate signature
    response = requests.get(
        '/hmac_auth_view',
        headers={hmac.header: sig}
    )

To generate signature for particular service:

.. sourcecode:: python

    sig = shmac.make_hmac_for('service', 'request body')
    response = requests.get(
        '/hmac_auth_view',
        'request body',
        headers={hmac.header: sig}
    )


HTTP
----

Valid signature is send:
~~~~~~~~~~~~~~~~~~~~~~~~

**Example request**:

.. sourcecode:: http

    GET /api/v1/users HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Host: localdocker:8000
    Signature: dXNlcnNlcnZpY2U6RDVyRm5TcnJUUTQyZUttcDIreWhXayttYzZPK0hjRHZjWWFwbW9MeFdjQT0=
    User-Agent: HTTPie/0.9.2


**Response response**:

.. sourcecode:: http

    HTTP/1.0 200 OK
    Content-Type: text/html; charset=utf-8
    Date: Thu, 15 Oct 2015 09:53:10 GMT
    Server: WSGIServer/0.1 Python/2.7.10
    Vary: Cookie
    X-Frame-Options: SAMEORIGIN


Invalid signature is send:
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Response request**:

.. sourcecode:: http

    GET /api/v1/users HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Host: localdocker:8000
    Signature: blabla
    User-Agent: HTTPie/0.9.2


**Response response**:

.. sourcecode:: http

    HTTP/1.0 403 FORBIDDEN
    Content-Type: text/html; charset=utf-8
    Date: Thu, 15 Oct 2015 09:53:35 GMT
    Server: WSGIServer/0.1 Python/2.7.10
    Vary: Cookie
    X-Frame-Options: SAMEORIGIN
