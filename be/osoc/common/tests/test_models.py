"""
Unit tests for models.py
"""
from django.test import TestCase
from osoc.common.tests import CoachFactory, ProjectFactory, SentEmailFactory, SkillFactory, StudentFactory
from osoc.common.models import Student, Skill, Coach, Project, Suggestion, SentEmail


class SkillTests(TestCase):
    """
    test class for testing skill model methods
    """
    def setUp(self):
        """
        test setup
        """
        SkillFactory(name="skill")

    def test_str(self):
        """
        test __str()__ method
        """
        skill = Skill.objects.first()
        self.assertEqual(str(skill), skill.name)
        self.assertEqual(str(skill), "skill")


class CoachManagerTests(TestCase):
    """
    test class for testing coachmanager model methods
    """
    def test_create_user(self):
        """
        test create_user() method
        """
        Coach.objects.create_user(
            email="email@example.com",
            password="password",
            first_name="john",
            last_name="doe"
        )
        coach = Coach.objects.get(email="email@example.com")
        self.assertIsNotNone(coach)
        self.assertEqual(coach.first_name, "john")

    def test_create_user_email_not_set(self):
        """
        test create_user() method without an email
        """
        with self.assertRaises(ValueError):
            Coach.objects.create_user(
                email="",
                password="password",
                first_name="john",
                last_name="doe"
            )
            coach = Coach.objects.get(first_name="john")
            self.assertIsNone(coach)

    def test_create_superuser(self):
        """
        test create_superuser() method
        """
        Coach.objects.create_superuser(
            email="email@example.com",
            password="password",
            first_name="john",
            last_name="doe"
        )
        coach = Coach.objects.get(email="email@example.com")
        self.assertIsNotNone(coach)
        self.assertEqual(coach.first_name, "john")
        self.assertEqual(coach.is_staff, True)
        self.assertEqual(coach.is_superuser, True)
        self.assertEqual(coach.is_active, True)


class CoachTests(TestCase):
    """
    test class for testing coach model methods
    """
    def setUp(self):
        """
        test setup
        """
        Coach.objects.create_user(
            email="  Email@EXAMPLE.com",
            first_name=" John  ",
            last_name="    Doe   ",
            password="password"
        )

    def test_full_name(self):
        """
        test get_full_name() method
        """
        coach = Coach.objects.first()
        self.assertEqual(coach.get_full_name(), "John Doe")

    def test_clean(self):
        """
        test clean() method
        """
        coach = Coach.objects.first()
        self.assertEqual(coach.email, "email@example.com")
        self.assertEqual(coach.first_name, "John")
        self.assertEqual(coach.last_name, "Doe")

    def test_str(self):
        """
        test __str__() method
        """
        coach = Coach.objects.first()
        self.assertEqual(str(coach), coach.get_full_name())
        self.assertEqual(str(coach), "John Doe")


class StudentTests(TestCase):
    """
    test class for testing student model methods
    """
    def setUp(self):
        """
        test setup
        """
        StudentFactory(
            first_name="   Jane   ",
            last_name="  Doe   "
        )

    def test_full_name(self):
        """
        test get_full_name() method
        """
        student = Student.objects.first()
        self.assertEqual(student.get_full_name(), "Jane Doe")

    def test_clean(self):
        """
        test clean() method
        """
        student = Student.objects.first()
        self.assertEqual(student.first_name, "Jane")
        self.assertEqual(student.last_name, "Doe")

    def test_str(self):
        """
        test __str__() method
        """
        student = Student.objects.first()
        self.assertEqual(str(student), student.get_full_name())
        self.assertEqual(str(student), "Jane Doe")


class ProjectTests(TestCase):
    """
    test class for testing project model methods
    """
    def setUp(self):
        """
        test setup
        """
        ProjectFactory(name="project")

    def test_str(self):
        """
        test __str__() method
        """
        project = Project.objects.first()
        self.assertEqual(str(project), project.name)
        self.assertEqual(str(project), "project")


class SuggestionTests(TestCase):
    """
    test class for testing suggestion model methods
    """
    def setUp(self):
        """
        test setup
        """
        coach = CoachFactory()
        student = StudentFactory()
        Suggestion.objects.create(
            suggestion="0",
            reason="a reason",
            coach=coach,
            student=student
        )

    def test_str(self):
        """
        test __str__() method
        """
        suggestion = Suggestion.objects.first()
        suggestion_str = f"{Suggestion.Suggestion(suggestion.suggestion).label}: {suggestion.reason}"
        self.assertEqual(str(suggestion), suggestion_str)
        self.assertEqual(str(suggestion), "Yes: a reason")


class SentEmailTests(TestCase):
    """
    test class for testing sentemail model methods
    """
    def setUp(self):
        """
        test setup
        """
        coach = CoachFactory(first_name="John", last_name="Doe")
        student = StudentFactory(first_name="Jane", last_name="Doe")
        SentEmailFactory(sender=coach, receiver=student, info="email info")

    def test_str(self):
        """
        test __str__() method
        """
        email = SentEmail.objects.first()
        email_str = f"{email.info} (from: {email.sender}, to: {email.receiver})"
        self.assertEqual(str(email), email_str)
        self.assertEqual(str(email), "email info (from: John Doe, to: Jane Doe)")
