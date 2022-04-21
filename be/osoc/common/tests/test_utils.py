"""
Unit tests for utils.py
"""
from django.test import TestCase
from osoc.common.utils import *


class UtilityTestCases(TestCase):
    def test_strip_and_lower_email(self):
        correct_email = 'admin@example.com'
        test_email = strip_and_lower_email('  Admin@Example.com    ')
        self.assertEqual(correct_email, test_email)
