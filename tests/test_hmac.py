# Third Party Libs
from django.test import RequestFactory, TestCase

# First Party Libs
from djangohmac.sign import Hmac, InvalidSignature, UnknownKeyName


class HmacTestCase(TestCase):

    def setUp(self):
        self.hmac = Hmac()
        self.hmac.hmac_keys['serviceB'] = 'secret key for service b'
        self.factory = RequestFactory()
        self.header = 'HTTP_' + self.hmac.header.upper()

    def test_signature_is_not_empty(self):
        assert self.hmac.make_hmac()

    def test_signature_is_different_for_different_data(self):
        assert self.hmac.make_hmac('a') != self.hmac.make_hmac('b')

    def test_custom_secret_key(self):
        assert self.hmac.make_hmac(key='a') == self.hmac.make_hmac(key='a')
        assert self.hmac.make_hmac(key='a') != self.hmac.make_hmac(key='b')

    def test_valid_multiple_signatures_should_pass(self):
        signature = self.hmac.make_hmac_for('serviceA')
        request = self.factory.get('/example', **{self.header: signature})
        assert self.hmac.validate_signature(request)

    def test_invalid_multiple_signatures_should_raice_exception(self):
        signature = self.hmac.make_hmac_for('serviceA', 'some data')
        request = self.factory.get('/example', **{self.header: signature})
        with self.assertRaises(InvalidSignature):
            self.hmac.validate_signature(request)

    def test_unknown_key_name_for_multiple_signatures_should_raice_exception(self):
        with self.assertRaises(UnknownKeyName):
            self.hmac.make_hmac_for('unknown')

    def test_valid_signature_for_services_are_restricted_view(self):
        signature = self.hmac.make_hmac_for('serviceB')
        request = self.factory.get('/example', **{self.header: signature})
        with self.assertRaises(InvalidSignature):
            self.hmac.validate_signature(
                request,
                only=['serviceA']
            )

    def test_valid_signature_for_resticted_view(self):
        signature = self.hmac.make_hmac()
        request = self.factory.get('/example', **{self.header: signature})
        with self.assertRaises(InvalidSignature):
            self.hmac.validate_signature(
                request,
                only=['serviceA']
            )
