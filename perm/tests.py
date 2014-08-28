from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.unittest import TestCase
from django.db import models

from .decorators import permissions_for
from .permissions import ModelPermissions
from .exceptions import PermAppException
from .utils import get_model


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def user_can_visit(self, user):
        return user.is_staff


@permissions_for(Person)
class PersonPermissions(ModelPermissions):
    def has_perm_visit(self):
        # Let's ask the Person object
        return self.obj.user_can_visit(self.user)

    def get_perm_mirror_queryset(self):
        # Foo objects can be changed by their owners
        return Person.objects.filter(first_name=self.user.username)


class UtilsTest(TestCase):
    def test_get_model(self):
        with self.assertRaises(PermAppException):
            get_model('does.NotExist', raise_exception=True)
        self.assertEqual(None, get_model('does.NotExist', raise_exception=False))
        self.assertEqual(Person, get_model('perm.Person', raise_exception=False))


class PermissionsTest(TestCase):
    def setUp(self):
        person_alpha = Person.objects.create(first_name='alpha', last_name='centauri')
        self.alpha = User.objects.create(username='alpha', is_superuser=True, is_staff=False)
        self.beta = User.objects.create(username='beta', is_superuser=False, is_staff=True)
        self.gamma = User.objects.create(username='gamma', is_superuser=False, is_staff=False)

    def test_permission_does_not_exist(self):
        pass

    def tearDown(self):
        self.alpha.delete()
        self.beta.delete()
        self.gamma.delete()