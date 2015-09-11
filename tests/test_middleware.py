from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from djangohmac.middleware import HmacMiddleware
from djangohmac.sign import Hmac


class MiddlewareTestCase(TestCase):

    def setUp(self):
        self.hmacmiddleware = HmacMiddleware()
        self.factory = RequestFactory()
        self.hmac = Hmac()

    def test_raise_exception_when_signature_is_not_send(self):
        request = self.factory.get('/example',)
        with self.assertRaises(PermissionDenied):
            self.hmacmiddleware.process_request(request)

    def test_should_be_ok_when_right_hmac_is_send(self):
        signature = self.hmac.make_hmac()
        request = self.factory.get('/example', **{self.hmac.header: signature})
        self.hmacmiddleware.process_request(request)

    def test_raise_exception_when_invalid_hmac_is_send(self):
        request = self.factory.get('/example', **{self.hmac.header: '00'})

        with self.assertRaises(PermissionDenied):
            self.hmacmiddleware.process_request(request)
