from __future__ import unicode_literals

from django.utils.unittest import TestCase

from .exceptions import PermAppException
from .utils import get_model


class UtilsTest(TestCase):

    def test_get_model(self):
        with self.assertRaises(PermAppException):
            get_model('does.NotExist', raise_exception=True)
        self.assertEqual(None, get_model('does.NotExist', raise_exception=False))
