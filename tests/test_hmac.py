# Third Party Libs
# from django.core.urlresolvers import reverse
from django.test import TestCase
from djangohmac.sign import Hmac


class HmacTestCase(TestCase):

    def setUp(self):
        self.hmac = Hmac()

    def test_signature_is_not_empty(self):
        assert self.hmac.make_hmac()

    def test_signature_is_different_for_different_data(self):
        assert self.hmac.make_hmac('a') != self.hmac.make_hmac('b')
