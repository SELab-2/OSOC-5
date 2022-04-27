"""
Unit tests for utils.py
"""
from django.test import TestCase
from django.utils import timezone
from osoc.common.utils import *


class UtilityTestCases(TestCase):
    def test_strip_and_lower_email(self):
        correct_email = 'admin@example.com'
        test_email = strip_and_lower_email('  Admin@Example.com    ')
        self.assertEqual(correct_email, test_email)

    def test_string_to_datetime_tz(self):
        string = "2022-01-03"
        date = string_to_datetime_tz(string)
        correct_date = timezone.make_aware(timezone.datetime(2022, 1, 3))
        self.assertEqual(date, correct_date)

        string = "2022-09-06T05:04:23"
        date = string_to_datetime_tz(string)
        correct_date = timezone.make_aware(timezone.datetime(2022, 9, 6, 5, 4, 23))
        self.assertEqual(date, correct_date)

        # wrong formats
        with self.assertRaises(ValueError):
            string = "2022-13-13"
            date = string_to_datetime_tz(string)

        with self.assertRaises(ValueError):
            string = "2022-04-01T25:75:98"
            date = string_to_datetime_tz(string)
        
        with self.assertRaises(ValueError):
            string = "not-a-date"
            date = string_to_datetime_tz(string)
    
    def test_reverse_querystring(self):
        url = reverse_querystring("student-list", query_kwargs=({"on_project": "true"}))
        correct_url = reverse("student-list") + "?on_project=true"
        self.assertEqual(url, correct_url)

        url = reverse_querystring("student-list")
        correct_url = reverse("student-list")
        self.assertEqual(url, correct_url)
