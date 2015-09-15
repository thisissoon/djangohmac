# Third Party Libs
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

# First Party Libs
from djangohmac.middleware import GlobalHmacMiddleware, MultipleHmacMiddleware
from djangohmac.sign import Hmac


class GlobalHmacMiddlewareTestCase(TestCase):

    def setUp(self):
        self.hmacmiddleware = GlobalHmacMiddleware()
        self.factory = RequestFactory()
        self.hmac = Hmac()

    def test_raise_exception_when_signature_is_not_send(self):
        request = self.factory.get('/example',)
        with self.assertRaises(PermissionDenied):
            self.hmacmiddleware.process_request(request)

    def test_should_be_ok_when_correct_hmac_is_send(self):
        signature = self.hmac.make_hmac()
        request = self.factory.get('/example', **{self.hmac.header: signature})
        self.hmacmiddleware.process_request(request)

    def test_raise_exception_when_invalid_hmac_is_send(self):
        request = self.factory.get('/example', **{self.hmac.header: '00'})

        with self.assertRaises(PermissionDenied):
            self.hmacmiddleware.process_request(request)


class MultipleHmacMiddlewareTestCase(TestCase):

    def setUp(self):
        self.hmacmiddleware = MultipleHmacMiddleware()
        self.factory = RequestFactory()
        self.hmac = Hmac()

    def test_raise_exception_when_signature_is_not_send(self):
        request = self.factory.get('/example',)
        with self.assertRaises(PermissionDenied):
            self.hmacmiddleware.process_request(request)

    def test_should_be_ok_when_correct_hmac_is_send(self):
        signature = self.hmac.make_hmac_for('service')
        request = self.factory.get('/example', **{self.hmac.header: signature})
        self.hmacmiddleware.process_request(request)

    def test_raise_exception_when_signature_changed(self):
        signature = self.hmac.make_hmac_for('service', 'some data')
        request = self.factory.get('/example', **{self.hmac.header: signature})

        with self.assertRaises(PermissionDenied):
            self.hmacmiddleware.process_request(request)

    def test_raise_exception_when_invalid_hmac_is_send(self):
        request = self.factory.get('/example', **{self.hmac.header: '00'})

        with self.assertRaises(PermissionDenied):
            self.hmacmiddleware.process_request(request)
