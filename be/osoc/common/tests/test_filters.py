"""
Unit tests for filters.py
"""
# pylint: disable=duplicate-code,too-many-lines
from rest_framework.test import APITestCase
from django.utils import timezone
from osoc.common.tests import AdminFactory, CoachFactory, ProjectFactory, SentEmailFactory, SkillFactory, StudentFactory
from osoc.common.utils import reverse_querystring
from osoc.common.models import Project, ProjectSuggestion, Skill, Suggestion, Student

class StudentFilterTests(APITestCase):
    """
    test class for testing custom student filters
    """
    def setUp(self):
        """
        test setup
        """
        self.user = AdminFactory()
        self.client.force_authenticate(self.user)

        StudentFactory()
        StudentFactory(email="email2@example.com")
        StudentFactory(email="email3@example.com")

    def test_multiple_status_filter(self):
        """
        test GET /students/?status=
        """
        first = Student.objects.first()
        first.status = 1
        first.save()
        second = Student.objects.exclude(id=first.id).first()
        second.status = 2
        second.save()

        url = reverse_querystring("student-list", query_kwargs=({"status": "1,2"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 2)

    def test_student_on_project_filter(self):
        """
        test GET /students/?on_project=
        """
        # add a student to a project
        student = Student.objects.first()
        project = ProjectFactory()
        skill = SkillFactory()
        project.required_skills.add(skill)
        ProjectSuggestion.objects.create(
            project=project,
            student=student,
            skill=skill,
            coach=self.user
        )

        url = reverse_querystring("student-list", query_kwargs=({"on_project": "true"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)

        url = reverse_querystring("student-list", query_kwargs=({"on_project": "false"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 2)

    def test_student_suggested_by_user(self):
        """
        test GET /students/?suggested_by_user=
        """
        # make suggestion for student by user
        student = Student.objects.first()
        Suggestion.objects.create(
            student=student,
            coach=self.user
        )
        # make suggestion for another student by another coach
        coach = CoachFactory(email="coach2@example.com")
        # different student
        student2 = Student.objects.exclude(id=student.id).first()
        Suggestion.objects.create(
            student=student2,
            coach=coach
        )

        url = reverse_querystring("student-list", query_kwargs=({"suggested_by_user": "true"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)

        url = reverse_querystring("student-list", query_kwargs=({"suggested_by_user": "false"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 2)

    def test_student_final_decision_filter(self):
        """
        test GET /students/?suggestion=
        """
        # make final decision
        student = Student.objects.first()
        suggestion = Suggestion.objects.create(
            suggestion=Suggestion.Suggestion.YES,
            student=student,
            coach=self.user,
            final=True
        )
        student.final_decision = suggestion
        student.save()

        url = reverse_querystring("student-list", query_kwargs=({"suggestion": "yes"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)

        url = reverse_querystring("student-list", query_kwargs=({"suggestion": "undecided"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 2)

    def test_student_conflict_filter(self):
        """
        test GET /students/?conflicting=
        """
        project1 = ProjectFactory()
        project2 = ProjectFactory(name="project2")
        skill = SkillFactory()
        project1.required_skills.add(skill)
        project2.required_skills.add(skill)

        student1 = Student.objects.first()
        student2 = Student.objects.exclude(id=student1.id).first()

        # assign a student to 2 different projects
        ProjectSuggestion.objects.create(
            project=project1,
            student=student1,
            skill=skill,
            coach=self.user
        )
        ProjectSuggestion.objects.create(
            project=project2,
            student=student1,
            skill=skill,
            coach=self.user
        )
        # assign a student twice to the same project
        ProjectSuggestion.objects.create(
            project=project1,
            student=student2,
            skill=skill,
            coach=self.user
        )
        skill2 = SkillFactory(name="skill2")
        ProjectSuggestion.objects.create(
            project=project1,
            student=student2,
            skill=skill2,
            coach=self.user
        )

        url = reverse_querystring("student-list", query_kwargs=({"conflicting": "true"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 2)

        url = reverse_querystring("student-list", query_kwargs=({"conflicting": "false"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)


class EmailFilterTests(APITestCase):
    """
    test class for testing custom email filters
    """
    def setUp(self):
        """
        test setup
        """
        self.user = AdminFactory()
        student = StudentFactory()
        self.client.force_authenticate(self.user)
        for day in range(1, 6):
            SentEmailFactory(
                sender=self.user,
                receiver=student,
                time=timezone.make_aware(timezone.datetime(2022, 1, day, 12, 0, 0))
            )

    def test_email_datetime_filter_date(self):
        """
        test GET /sentemails/?date=
        """
        url = reverse_querystring("sentemail-list", query_kwargs=({"date": "2022-01-01"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)

        url = reverse_querystring("sentemail-list", query_kwargs=({"date": "2022-02-01"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)

    def test_email_datetime_filter_before(self):
        """
        test GET /sentemails/?before=
        """
        url = reverse_querystring("sentemail-list", query_kwargs=({"before": "2022-01-03T13:00:00"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 3)

        url = reverse_querystring("sentemail-list", query_kwargs=({"before": "2022-01-01T11:00:00"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)

    def test_email_datetime_filter_after(self):
        """
        test GET /sentemails/?after=
        """
        url = reverse_querystring("sentemail-list", query_kwargs=({"after": "2022-01-02T12:00:00"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 3)

        url = reverse_querystring("sentemail-list", query_kwargs=({"after": "2022-01-07"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)

    def test_email_datetime_filter_wrong_format(self):
        """
        test GET /sentemails/?date= with wrong date format
        """
        url = reverse_querystring("sentemail-list", query_kwargs=({"date": "wrong format"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 5)


class ProjectFilterTests(APITestCase):
    """
    test class for testing custom project filters
    """
    def setUp(self):
        """
        test setup
        """
        self.user = AdminFactory()
        self.client.force_authenticate(self.user)

        projects = [ProjectFactory(name="project1"),
                    ProjectFactory(name="project2"),
                    ProjectFactory(name="project3")]

        skill = SkillFactory()
        for project in projects:
            project.required_skills.add(skill)

    def test_project_full_filter(self):
        """
        test GET /projects/?full=
        """
        skill = Skill.objects.first()
        project = Project.objects.first()
        student = StudentFactory()
        ProjectSuggestion.objects.create(
            project=project,
            student=student,
            skill=skill,
            coach=self.user
        )

        url = reverse_querystring("project-list", query_kwargs=({"full": "true"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)

        url = reverse_querystring("project-list", query_kwargs=({"full": "false"}))
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 2)
