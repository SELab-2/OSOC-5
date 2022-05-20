"""
Unit tests for utils.py
"""
from django.test import TestCase
from django.utils import timezone
from rest_framework.reverse import reverse
from osoc.common.serializers import CSVCoachSerializer, CSVProjectSerializer, CSVProjectSuggestionSerializer, CSVRequiredSkillSerializer, CSVSentEmailSerializer, CSVSkillSerializer, CSVStudentSerializer, CSVSuggestionSerializer
from osoc.common.tests import CoachFactory, ProjectFactory, SentEmailFactory, SkillFactory, StudentFactory
from osoc.common.models import Coach, Project, ProjectSuggestion, RequiredSkills, SentEmail, Skill, Student, Suggestion
from osoc.common.utils import export_to_csv, strip_and_lower_email, string_to_datetime_tz, reverse_querystring, get_nested


class UtilityTestCases(TestCase):
    """
    test class for testing utility functions
    """
    def test_strip_and_lower_email(self):
        """
        test strip_and_lower_email function
        """
        correct_email = 'admin@example.com'
        test_email = strip_and_lower_email('  Admin@Example.com    ')
        self.assertEqual(correct_email, test_email)

    def test_string_to_datetime_tz(self):
        """
        test string_to_datetime_tz function
        """
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
        """
        test reverse_querystring function
        """
        url = reverse_querystring("student-list", query_kwargs=({"on_project": "true"}))
        correct_url = reverse("student-list") + "?on_project=true"
        self.assertEqual(url, correct_url)

        url = reverse_querystring("student-list")
        correct_url = reverse("student-list")
        self.assertEqual(url, correct_url)

    def test_get_nested(self):
        """
        test get_nested function
        """
        self.assertEqual(None, get_nested({'a': {'b': True}}, None, 'a', 'c'))
        self.assertEqual(None, get_nested({'a': {'b': True}}, None, 'b', 'a'))
        self.assertEqual(True, get_nested({'a': {'b': True }}, None, 'a', 'b'))
        self.assertEqual(True, get_nested({'a': {'b': { 'c': True }}}, None, 'a', 'b', 'c'))

    def test_export_to_csv(self):
        """
        test export_to_csv function
        """
        # create objects
        student = StudentFactory()
        coach = CoachFactory()
        project = ProjectFactory()
        skill = SkillFactory()
        SentEmailFactory(
            sender=coach,
            receiver=student
        )
        Suggestion.objects.create(
            student=student,
            coach=coach,
            suggestion='0'
        )
        ProjectSuggestion.objects.create(
            student=student,
            project=project,
            coach=coach,
            skill=skill
        )
        RequiredSkills.objects.create(
            project=project,
            skill=skill
        )

        for model, serializer in [
                (Student, CSVStudentSerializer),
                (Coach, CSVCoachSerializer),
                (Project, CSVProjectSerializer),
                (Skill, CSVSkillSerializer),
                (SentEmail, CSVSentEmailSerializer),
                (Suggestion, CSVSuggestionSerializer),
                (ProjectSuggestion, CSVProjectSuggestionSerializer),
                (RequiredSkills, CSVRequiredSkillSerializer)
            ]:

            csv = export_to_csv(model.objects.all().order_by('id'), 'test', serializer)
            lines = csv.readlines()
            self.assertEqual(lines[0].strip().split(','), serializer.Meta.fields)
            self.assertEqual(len(lines), model.objects.count()+1)
            self.assertEqual(lines[1].strip().split(','),
                ['' if i is None else str(i) for i in serializer(model.objects.first()).data.values()])
