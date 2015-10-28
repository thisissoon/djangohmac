# Third Party Libs
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.views.generic import View
from djangohmac import decorators
from django.core.exceptions import PermissionDenied
from djangohmac.sign import shmac


class MethodDecoratedView(View):

    @decorators.auth
    def get(self, request):
        return HttpResponse("For all services")

    @decorators.auth(only=['serviceA'])
    def delete(self, request):
        return HttpResponse("Only for servvice A")


class MethodDecoratorTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.header = 'HTTP_' + shmac.header.upper()
        self.my_view = MethodDecoratedView.as_view()

    def test_raise_exception_when_signature_is_not_send(self):
        request = self.factory.get('/', '')

        with self.assertRaises(PermissionDenied):
            self.my_view(request)

    def test_pass_when_valid_signature_is_send(self):
        signature = shmac.make_hmac_for('serviceA')
        request = self.factory.get('/', **{self.header: signature})

        assert 200 == self.my_view(request).status_code

    def test_pass_when_valid_signature_is_send_for_restricted_view(self):
        signature = shmac.make_hmac_for('serviceA')
        request = self.factory.delete('/', **{self.header: signature})

        assert 200 == self.my_view(request).status_code

    def test_raise_exception_when_another_service_try_to_access_view(self):
        signature = shmac.make_hmac_for('serviceB')
        request = self.factory.delete('/', **{self.header: signature})

        with self.assertRaises(PermissionDenied):
            self.my_view(request)
