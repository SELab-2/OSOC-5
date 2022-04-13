"""
Django tests for API endpoints.
Running tests is different because the project uses Docker:
    1. Run all tests:
        `docker exec -it osoc-be python manage.py test osoc.common.tests`
    2. Run one test class:
        `docker exec -it osoc-be python manage.py test osoc.common.tests:<TESTCLASS>`
    3. Run a single test:
        `docker exec -it osoc-be python manage.py test osoc.common.tests:<TESTCLASS>.<TESTMETHOD>`
"""
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from osoc.common.models import Coach, Project, ProjectSuggestion, Skill, Student, Suggestion
import osoc.common.utils as utils

class UtilityTestCases(TestCase):
    def testStripAndLowerEmail(self):
        self.assertEqual('admin@example.com', utils.strip_and_lower_email('Admin@Example.com'))
        self.assertEqual('admin@example.com', utils.strip_and_lower_email('  Admin@Example.com    '))

class ProjectTestsCoach(APITestCase):
    def setUp(self) -> None:
        Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info"
        )
        Project.objects.create(
            name="Test_2",
            partner_name="Partner",
            extra_info="Exra info"
        )
        Student.objects.create(
            employment_agreement="volunteer",
            hinder_work="",
            first_name="First name",
            last_name="Last name",
            call_name="call name",
            gender=0,
            pronouns="",
            email="example@example.com",
            phone_number="+14255550123",
            language="Dutch",
            english_rating=3,
            motivation="extra info",
            cv="https://example.com",
            portfolio="https://example.com",
            fun_fact="I swim",
            school_name="Example",
            degree="Example",
            degree_duration=3,
            degree_current_year=1,
            studies="Example",
            best_skill="Example",
            alum=False,
            student_coach=True
        )
        Skill.objects.create(
            name="skill",
            description="a skill",
            color="blue"
        )

        user = Coach.objects.create_user(
            first_name="username", password="Pas$w0rd", last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

    def test_get_project_list(self):
        url = reverse("project-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Project.objects.count())

    def test_get_project_instance(self):
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], project.name)
        self.assertEqual(response.data["partner_name"], project.partner_name)
        self.assertEqual(response.data["extra_info"], project.extra_info)

    def test_get_project_instance_not_found(self):
        url = reverse("project-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_project_forbidden(self):
        data = {
            "name": "Test_3",
            "partner_name": "Partner",
            "extra_info": "Extra info",
            "required_skills": [],
            "coaches": []
        }
        url = reverse("project-list")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_project_forbidden(self):
        id = Project.objects.first().id
        url = reverse("project-detail", args=(id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_suggest_student(self):
        project = Project.objects.first()
        url = reverse("project-suggest-student", args=(project.id,))
        student = Student.objects.first()
        skill = Skill.objects.first()
        data = {
            "student": reverse("student-detail", args=(student.id,)),
            "role": reverse("skill-detail", args=(skill.id,)),
            "reason": "a reason"
        }
        before_count = ProjectSuggestion.objects.filter(project=project).count()
        response = self.client.post(url, data, format="json")
        after_count = ProjectSuggestion.objects.filter(project=project).count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count, after_count-1)

    def test_project_remove_student(self):
        project = Project.objects.first()
        url = reverse("project-suggest-student", args=(project.id,))
        student = Student.objects.first()
        skill = Skill.objects.first()
        data = {
            "student": reverse("student-detail", args=(student.id,)),
            "role": reverse("skill-detail", args=(skill.id,)),
            "reason": "a reason"
        }
        response = self.client.post(url, data, format="json")

        url = reverse("project-remove-student", args=(project.id,))
        before_count = ProjectSuggestion.objects.filter(project=project).count()
        response = self.client.post(url, data, format="json")
        after_count = ProjectSuggestion.objects.filter(project=project).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(before_count, after_count+1)


class ProjectTestsAdmin(APITestCase):
    def setUp(self) -> None:
        Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info"
        )
        Skill.objects.create(
            name="skill",
            description="a skill",
            color="blue"
        )

        admin = Coach.objects.create_user(
            first_name="admin", password="Pas$w0rd", last_name="last_name", email="admin@example.com", is_admin=True)
        self.client.force_authenticate(admin)

    def test_create_project(self):
        skill = Skill.objects.first()
        coach = Coach.objects.first()
        data = {
            "name": "Test_2",
            "partner_name": "Partner",
            "extra_info": "Extra info",
            "required_skills": [{"skill": reverse("skill-detail", args=(skill.id,)), "amount": "2"}],
            "coaches": [reverse("coach-detail", args=(coach.id,))]
        }
        url = reverse("project-list")
        before_count = Project.objects.count()
        response = self.client.post(url, data, format="json")
        after_count = Project.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(before_count, after_count-1)

    def test_create_project_bad_request(self):
        url = reverse("project-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self):
        id = Project.objects.first().id
        url = reverse("project-detail", args=(id,))
        before_count = Project.objects.count()
        response = self.client.delete(url)
        after_count = Project.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_project_not_found(self):
        url = reverse("project-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SkillTests(APITestCase):
    def setUp(self):
        Skill.objects.create(
            name="skill",
            description="a skill",
            color="blue"
        )
        Skill.objects.create(
            name="skill_2",
            description="another skill",
            color="red"
        )

        user = Coach.objects.create_user(
            first_name="username", password="Pas$w0rd", last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

    def test_get_skill_list(self):
        url = reverse("skill-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Skill.objects.count())

    def test_get_skill_instance(self):
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], skill.name)
        self.assertEqual(response.data["description"], skill.description)

    def test_get_skill_instance_not_found(self):
        url = reverse("skill-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_skill(self):
        id = Skill.objects.first().id
        url = reverse("skill-detail", args=(id,))
        before_count = Skill.objects.count()
        response = self.client.delete(url)
        after_count = Skill.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_skill_not_found(self):
        url = reverse("skill-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_skill(self):
        data = {
            "name": "skill_3",
            "description": "yet another skill",
            "color": "green"
        }
        url = reverse("skill-list")
        before_count = Skill.objects.count()
        response = self.client.post(url, data, format="json")
        after_count = Skill.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(before_count, after_count-1)

    def test_create_skill_bad_request(self):
        url = reverse("skill-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StudentTests(APITestCase):
    def setUp(self) -> None:
        Student.objects.create(
            employment_agreement="volunteer",
            hinder_work="",
            first_name="First name",
            last_name="Last name",
            call_name="call name",
            gender=0,
            pronouns="",
            email="example@example.com",
            phone_number="+14255550123",
            language="Dutch",
            english_rating=3,
            motivation="extra info",
            cv="https://example.com",
            portfolio="https://example.com",
            fun_fact="I swim",
            school_name="Example",
            degree="Example",
            degree_duration=3,
            degree_current_year=1,
            studies="Example",
            best_skill="Example",
            alum=False,
            student_coach=True
        )
        Skill.objects.create(
            name="skill",
            description="a skill",
            color="blue"
        )

        user = Coach.objects.create_user(
            first_name="username", password="Pas$w0rd", last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

    def test_get_student_list(self):
        url = reverse("student-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Student.objects.count())

    def test_get_student_instance(self):
        student = Student.objects.first()
        url = reverse("student-detail", args=(student.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], student.email)

    def test_get_student_instance_not_found(self):
        url = reverse("student-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_student(self):
        id = Student.objects.first().id
        url = reverse("student-detail", args=(id,))
        before_count = Student.objects.count()
        response = self.client.delete(url)
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_student_not_found(self):
        url = reverse("student-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_student(self):
        skill = Skill.objects.first()
        data = {
            "employment_agreement": "student",
            "first_name": "John",
            "last_name": "Doe",
            "gender": 1,
            "email": "john.doe@example.com",
            "motivation": "I like work",
            "cv": "https://example.com",
            "portfolio": "https://example.com",
            "language": "Dutch",
            "fun_fact": "I cycle",
            "school_name": "Example",
            "degree": "Example",
            "degree_duration": 5,
            "degree_current_year": 2,
            "studies": "Example",
            "skills": [reverse("skill-detail", args=(skill.id,))],
            "best_skill": "frontend"
        }
        url = reverse("student-list")
        before_count = Student.objects.count()
        response = self.client.post(url, data, format="json")
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(before_count, after_count-1)

    def test_create_student_bad_request(self):
        url = reverse("student-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_make_suggestion(self):
        student = Student.objects.first()
        url = reverse("student-make-suggestion", args=(student.id,))
        data = {"suggestion": "0", "reason": "a reason"}
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.post(url, data, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count, after_count-1)

    def test_student_make_suggestion_bad_request(self):
        student = Student.objects.first()
        url = reverse("student-make-suggestion", args=(student.id,))
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CoachTestsCoach(APITestCase):
    def setUp(self):
        Coach.objects.create(
            first_name="first name",
            last_name="last name",
            password="p4ssWorD",
            email="email2@example.com"
        )

        self.user = Coach.objects.create_user(
            first_name="username",
            password="Pas$w0rd",
            last_name="last_name",
            email="email@example.com")
        self.client.force_authenticate(self.user)

    def test_get_coach_list_forbidden(self):
        url = reverse("coach-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coach_instance_forbidden(self):
        coach = Coach.objects.exclude(id=self.user.id).first()
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coach_instance_owner(self):
        coach = self.user
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], coach.email)

    def test_update_coach_forbidden(self):
        coach = Coach.objects.exclude(id=self.user.id).first()
        old_name = coach.first_name
        url = reverse("coach-detail", args=(coach.id,))
        data = {
            "first_name": "new first name",
            "last_name": "last name",
            "email": "email2@example.com"
        }
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coach.first_name, old_name)

    def test_update_coach_owner(self):
        coach = self.user
        url = reverse("coach-detail", args=(coach.id,))
        data = {
            "first_name": "new first name",
            "last_name": "last name",
            "email": "email@example.com"
        }
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])
        # Is it possible to update 'coach' variable with latest info from database?
        self.assertEqual(Coach.objects.get(id=self.user.id).first_name, data["first_name"])

    def test_get_coach_instance_not_found(self):
        url = reverse("coach-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_coach_forbidden(self):
        coach_id = Coach.objects.first().id
        url = reverse("coach-detail", args=(coach_id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CoachTestsAdmin(APITestCase):
    def setUp(self):
        Coach.objects.create(
            first_name="first name",
            last_name="last name",
            password="p4ssWorD",
            email="email2@example.com"
        )

        self.admin = Coach.objects.create_user(
            first_name="admin",
            password="Pas$w0rd",
            last_name="last_name",
            email="admin@example.com",
            is_admin=True)
        self.client.force_authenticate(self.admin)

    def test_coach_list(self):
        url = reverse("coach-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Coach.objects.count())

    def test_coach_instance(self):
        coach = Coach.objects.exclude(id=self.admin.id).first()
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_coach(self):
        id = Coach.objects.first().id
        url = reverse("coach-detail", args=(id,))
        before_count = Coach.objects.count()
        response = self.client.delete(url)
        after_count = Coach.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_coach_not_found(self):
        url = reverse("coach-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_coach_make_admin(self):
        coach = Coach.objects.exclude(id=self.admin.id).first()
        coach.is_admin = False
        coach.save()
        url = reverse("coach-make-admin", args=(coach.id,))
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Coach.objects.get(id=coach.id).is_admin, True)

    def test_coach_remove_admin(self):
        coach = Coach.objects.exclude(id=self.admin.id).first()
        coach.is_admin = True
        coach.save()
        url = reverse("coach-remove-admin", args=(coach.id,))
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Coach.objects.get(id=coach.id).is_admin, False)
