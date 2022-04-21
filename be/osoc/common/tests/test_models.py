"""
Unit tests for models.py
"""
from django.dispatch import receiver
from django.test import TestCase
from osoc.common.models import *


class SkillTests(TestCase):
    def setUp(self):
        Skill.objects.create(
            name="skill"
        )

    def test_str(self):
        skill = Skill.objects.first()
        self.assertEqual(str(skill), skill.name)
        self.assertEqual(str(skill), "skill")


class CoachManagerTests(TestCase):
    def test_create_user(self):
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
    def setUp(self):
        Coach.objects.create_user(
            email="  Email@EXAMPLE.com",
            password="password",
            first_name=" John  ",
            last_name="    Doe   "
        )

    def test_full_name(self):
        coach = Coach.objects.first()
        self.assertEqual(coach.get_full_name(), "John Doe")
    
    def test_clean(self):
        coach = Coach.objects.first()
        self.assertEqual(coach.email, "email@example.com")
        self.assertEqual(coach.first_name, "John")
        self.assertEqual(coach.last_name, "Doe")

    def test_str(self):
        coach = Coach.objects.first()
        self.assertEqual(str(coach), coach.get_full_name())
        self.assertEqual(str(coach), "John Doe")


class StudentTests(TestCase):
    def setUp(self):
        Student.objects.create(
            first_name="   Jane   ",
            last_name="  Doe   ",
            call_name="call name",
            email="email@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )
    
    def test_full_name(self):
        student = Student.objects.first()
        self.assertEqual(student.get_full_name(), "Jane Doe")
    
    def test_clean(self):
        student = Student.objects.first()
        self.assertEqual(student.email, "email@example.com")
        self.assertEqual(student.first_name, "Jane")
        self.assertEqual(student.last_name, "Doe")

    def test_str(self):
        student = Student.objects.first()
        self.assertEqual(str(student), student.get_full_name())
        self.assertEqual(str(student), "Jane Doe")


class ProjectTests(TestCase):
    def setUp(self):
        Project.objects.create(
            name="project"
        )

    def test_str(self):
        project = Project.objects.first()
        self.assertEqual(str(project), project.name)
        self.assertEqual(str(project), "project")


class SuggestionTests(TestCase):
    def setUp(self):
        coach = Coach.objects.create_user(
            email="  Email@EXAMPLE.com",
            password="password",
            first_name=" John  ",
            last_name="    Doe   "
        )
        student = Student.objects.create(
            first_name="   Jane   ",
            last_name="  Doe   ",
            call_name="call name",
            email="email@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )
        Suggestion.objects.create(
            suggestion="0",
            reason="a reason",
            coach=coach,
            student=student
        )

    def test_str(self):
        suggestion = Suggestion.objects.first()
        suggestion_str = f"{Suggestion.Suggestion(suggestion.suggestion).label}: {suggestion.reason}"
        self.assertEqual(str(suggestion), suggestion_str)
        self.assertEqual(str(suggestion), "Yes: a reason")


class SentEmailTests(TestCase):
    def setUp(self):
        coach = Coach.objects.create_user(
            email="  Email@EXAMPLE.com",
            password="password",
            first_name=" John  ",
            last_name="    Doe   "
        )
        student = Student.objects.create(
            first_name="   Jane   ",
            last_name="  Doe   ",
            call_name="call name",
            email="email@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )
        SentEmail.objects.create(
            sender=coach,
            receiver=student,
            info="email info"
        )
    
    def test_str(self):
        email = SentEmail.objects.first()
        email_str = f"{email.info} (from: {email.sender}, to: {email.receiver})"
        self.assertEqual(str(email), email_str)
        self.assertEqual(str(email), "email info (from: John Doe, to: Jane Doe)")
