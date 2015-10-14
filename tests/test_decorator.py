# Third Party Libs
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.views.generic import View
from djangohmac import decorators
from django.core.exceptions import PermissionDenied
from djangohmac.sign import shmac


class SignedViewView(View):

    @decorators.auth()
    def get(self, request):
        return HttpResponse("For all services")

    @decorators.auth(only=['serviceA'])
    def delete(self, request):
        return HttpResponse("Only for servvice A")


class DecoratorsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.header = 'HTTP_' + shmac.header.upper()

    def test_raise_exception_when_signature_is_not_send(self):
        request = self.factory.get('/', '')
        my_view = SignedViewView.as_view()

        with self.assertRaises(PermissionDenied):
            my_view(request)

    def test_pass_when_valid_signature_is_send(self):
        signature = shmac.make_hmac_for('serviceA')
        request = self.factory.get('/', **{self.header: signature})
        my_view = SignedViewView.as_view()

        assert 200 == my_view(request).status_code

    def test_pass_when_valid_signature_is_send_for_restricted_view(self):
        signature = shmac.make_hmac_for('serviceA')
        request = self.factory.delete('/', **{self.header: signature})
        my_view = SignedViewView.as_view()

        assert 200 == my_view(request).status_code

    def test_raise_exception_when_another_service_try_to_access_view(self):
        signature = shmac.make_hmac_for('serviceB')
        request = self.factory.delete('/', **{self.header: signature})
        my_view = SignedViewView.as_view()

        with self.assertRaises(PermissionDenied):
            my_view(request)
