"""
Unit tests for filters.py
"""
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.utils import reverse_querystring
from osoc.common.filters import *
from osoc.common.models import Coach, ProjectSuggestion, Skill, Student, Project

class StudentFilterTests(APITestCase):
    def setUp(self):
        self.user = Coach.objects.create_user(
            first_name="username",
            last_name="last_name",
            email="user@example.com",
            password="Pas$w0rd",
            is_admin=True
        )
        self.client.force_authenticate(self.user)

        Student.objects.create(
            first_name="John",
            last_name="Doe",
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
        Student.objects.create(
            first_name="Jane",
            last_name="Doe",
            call_name="call name",
            email="email2@example.com",
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
        Student.objects.create(
            first_name="Jimmy",
            last_name="Doe",
            call_name="call name",
            email="email3@example.com",
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
    
    def test_student_on_project_filter(self):
        # add a student to a project
        student = Student.objects.first()
        project = Project.objects.create(name="project")
        skill = Skill.objects.create(name="skill")
        project.required_skills.add(skill)
        ProjectSuggestion.objects.create(
            project=project,
            student=student,
            skill=skill,
            coach=self.user
        )

        url = reverse_querystring("student-list", query_kwargs=({"on_project": "true"}))
        response = self.client.get(url)
        # there should be exactly 1 student returned
        self.assertEqual(len(response.data), 1)

        url = reverse_querystring("student-list", query_kwargs=({"on_project": "false"}))
        response = self.client.get(url)
        # there should be exactly 2 students returned
        self.assertEqual(len(response.data), 2)
    
    def test_student_suggested_by_user(self):
        # make suggestion for student by user
        student = Student.objects.first()
        Suggestion.objects.create(
            student=student,
            coach=self.user
        )
        # make suggestion for another student by another coach
        coach = Coach.objects.create_user(
            first_name="username",
            last_name="last_name",
            email="coach@example.com",
            password="Pas$w0rd"
        )
        # different student
        student2 = Student.objects.exclude(id=student.id).first()
        Suggestion.objects.create(
            student=student2,
            coach=coach
        )

        url = reverse_querystring("student-list", query_kwargs=({"suggested_by_user": "true"}))
        response = self.client.get(url)
        # there should be exactly 1 student returned
        self.assertEqual(len(response.data), 1)

        url = reverse_querystring("student-list", query_kwargs=({"suggested_by_user": "false"}))
        response = self.client.get(url)
        # there should be exactly 2 students returned
        self.assertEqual(len(response.data), 2)

    def test_student_final_decision_filter(self):
        # make final decision
        student = Student.objects.first()
        suggestion = Suggestion.objects.create(
            suggestion=Suggestion.Suggestion.YES,
            student=student,
            coach=self.user,
            final=True
        )
        student.final_decision = suggestion

        url = reverse_querystring("student-list", query_kwargs=({"suggestion": "yes"}))
        response = self.client.get(url)
        # there should be exactly 1 student returned
        self.assertEqual(len(response.data), 1)

        url = reverse_querystring("student-list", query_kwargs=({"suggestion": "none"}))
        response = self.client.get(url)
        # there should be exactly 2 students returned
        self.assertEqual(len(response.data), 2)
