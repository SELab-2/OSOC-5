"""
Integration tests for project API endpoints.

each test simulates an API call to one endpoint and checks if the response data and status code are correct
these tests test serializers.py and views.py and the API endpoints as a whole
"""
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import AdminFactory, CoachFactory, ProjectFactory, SkillFactory, StudentFactory
from osoc.common.models import Coach, Project, ProjectSuggestion, Skill, Student


class ProjectTestsCoach(APITestCase):
    """
    test class for testing project model by coach user (not all permissions)
    """
    def setUp(self) -> None:
        """
        test setup
        """
        skill = SkillFactory()
        project1 = ProjectFactory()
        project1.required_skills.add(skill)
        project2 = ProjectFactory(name="project2")
        project2.required_skills.add(skill)
        StudentFactory()
        self.user = CoachFactory()
        self.client.force_authenticate(self.user)

    def test_get_project_list(self):
        """
        test GET /projects/
        """
        url = reverse("project-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Project.objects.count())

    def test_get_project_instance(self):
        """
        test GET /projects/{id}/
        """
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], project.name)

    def test_get_project_instance_not_found(self):
        """
        test GET /projects/{id}/ with non-existing id
        """
        url = reverse("project-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_project_forbidden(self):
        """
        test POST /projects/ without permission
        """
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
        """
        test DELETE /projects/{id}/ without permission
        """
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_project_forbidden(self):
        """
        test PUT /projects/{id}/ without permission
        """
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_suggest_student(self):
        """
        test POST /projects/{id}/suggest_student
        """
        project = Project.objects.first()
        url = reverse("project-suggest-student", args=(project.id,))
        student = Student.objects.first()
        skill = project.required_skills.first()
        data = {
            "student": reverse("student-detail", args=(student.id,)),
            "skill": reverse("skill-detail", args=(skill.id,)),
            "reason": "a reason"
        }
        before_count = ProjectSuggestion.objects.filter(project=project).count()
        response = self.client.post(url, data, format="json")
        after_count = ProjectSuggestion.objects.filter(project=project).count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count, after_count-1)

    def test_project_suggest_student_skill_not_in_required_skills(self):
        """
        test POST /projects/{id}/suggest_student with a bad request
        """
        project = Project.objects.first()
        url = reverse("project-suggest-student", args=(project.id,))
        student = Student.objects.first()
        skill = SkillFactory(name="skill2")
        data = {
            "student": reverse("student-detail", args=(student.id,)),
            "skill": reverse("skill-detail", args=(skill.id,)),
            "reason": "a reason"
        }
        before_count = ProjectSuggestion.objects.filter(project=project).count()
        response = self.client.post(url, data, format="json")
        after_count = ProjectSuggestion.objects.filter(project=project).count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(before_count, after_count)

    def test_project_suggest_student_bad_request(self):
        """
        test POST /projects/{id}/suggest_student with a bad request
        """
        project = Project.objects.first()
        url = reverse("project-suggest-student", args=(project.id,))
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_remove_student(self):
        """
        test POST /projects/{id}/remove_student
        """
        project = Project.objects.first()
        url = reverse("project-suggest-student", args=(project.id,))
        student = Student.objects.first()
        skill = project.required_skills.first()
        data = {
            "student": reverse("student-detail", args=(student.id,)),
            "skill": reverse("skill-detail", args=(skill.id,)),
            "reason": "a reason"
        }
        response = self.client.post(url, data, format="json")

        url = reverse("project-remove-student", args=(project.id,))
        before_count = ProjectSuggestion.objects.filter(project=project).count()
        data = {
            "student": reverse("student-detail", args=(student.id,)),
            "skill": reverse("skill-detail", args=(skill.id,)),
            "coach": reverse("coach-detail", args=(self.user.id,))
        }
        response = self.client.post(url, data, format="json")
        after_count = ProjectSuggestion.objects.filter(project=project).count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_project_remove_student_bad_request(self):
        """
        test POST /projects/{id}/remove_student with a bad request
        """
        project = Project.objects.first()
        url = reverse("project-remove-student", args=(project.id,))
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_get_conflicting(self):
        """
        test GET /projects/get_conflicting_projects
        """
        # create conflict
        student = Student.objects.first()
        for project in Project.objects.all():
            url = reverse("project-suggest-student", args=(project.id,))
            skill = project.required_skills.first()
            data = {
                "student": reverse("student-detail", args=(student.id,)),
                "skill": reverse("skill-detail", args=(skill.id,))
            }
            self.client.post(url, data, format="json")

        url = reverse("project-get-conflicting-projects")
        response = self.client.get(url, format="json")

        self.assertEqual(response.data['count'], 1)

    def test_project_resolve_conflicts(self):
        """
        test POST /projects/resolve_conflicts
        """
        # create conflict
        student = Student.objects.first()
        for project in Project.objects.all():
            url = reverse("project-suggest-student", args=(project.id,))
            skill = project.required_skills.first()
            data = {
                "student": reverse("student-detail", args=(student.id,)),
                "skill": reverse("skill-detail", args=(skill.id,))
            }
            self.client.post(url, data, format="json")

        # resolve conflict
        url = reverse("project-resolve-conflicts")
        project = Project.objects.first()
        skill = project.required_skills.first()
        data = [{
            "project": reverse("project-detail", args=(project.id,)),
            "student": reverse("student-detail", args=(student.id,)),
            "skill": reverse("skill-detail", args=(skill.id,)),
            "coach": reverse("coach-detail", args=(self.user.id,))
        }]
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check there are no conflicts
        url = reverse("project-get-conflicting-projects")
        response = self.client.get(url)

        self.assertEqual(response.data['count'], 0)

    def test_project_resolve_conflicts_students_not_unique(self):
        """
        test POST /projects/resolve_conflicts with same students
        """
        url = reverse("project-resolve-conflicts")
        student = Student.objects.first()
        project = Project.objects.first()
        skill = project.required_skills.first()
        data = [{
            "project": reverse("project-detail", args=(project.id,)),
            "student": reverse("student-detail", args=(student.id,)),
            "skill": reverse("skill-detail", args=(skill.id,)),
            "coach": reverse("coach-detail", args=(self.user.id,))
        },
        {
            "project": reverse("project-detail", args=(project.id,)),
            "student": reverse("student-detail", args=(student.id,)),
            "skill": reverse("skill-detail", args=(skill.id,)),
            "coach": reverse("coach-detail", args=(self.user.id,))
        }]
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_resolve_conflicts_bad_request(self):
        """
        test POST /projects/resolve_conflicts with same students
        """
        url = reverse("project-resolve-conflicts")
        data = [{
            "project": "not an url"
        }]
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_all_forbidden(self):
        """
        test DELETE /projects/delete_all without permission
        """
        url = reverse("project-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_export_csv_forbidden(self):
        """
        test GET /projects/export_csv without permission
        """
        url = reverse("project-export-csv")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProjectTestsAdmin(APITestCase):
    """
    test class for testing project model by admin user (all permissions)
    """
    def setUp(self) -> None:
        """
        test setup
        """
        ProjectFactory()
        SkillFactory()
        admin = AdminFactory()
        self.client.force_authenticate(admin)

    def test_create_project(self):
        """
        test POST /projects/
        """
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
        """
        test POST /projects/ with a bad request
        """
        url = reverse("project-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self):
        """
        test DELETE /projects/{id}/
        """
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        before_count = Project.objects.count()
        response = self.client.delete(url)
        after_count = Project.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_project_not_found(self):
        """
        test DELETE /projects/{id}/ with a non-existing id
        """
        url = reverse("project-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project(self):
        """
        test PUT /projects/{id}/
        """
        project = Project.objects.first()
        skill = SkillFactory(name="skill2")
        coach = CoachFactory(email="coach2@example.com")
        data = {
            "name": "new project name",
            "partner_name": "partner",
            "extra_info": "info",
            "required_skills": [{"skill": reverse("skill-detail", args=(skill.id,)), "comment": "a comment", "amount": "3"}],
            "coaches": [reverse("coach-detail", args=(coach.id,))]
        }
        url = reverse("project-detail", args=(project.id,))
        response = self.client.put(url, data, format="json")
        project = Project.objects.get(id=project.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(project.name, data["name"])

    def test_delete_all(self):
        """
        test DELETE /projects/delete_all
        """
        url = reverse("project-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_export_csv(self):
        """
        test GET /projects/export_csv
        """
        url = reverse("project-export-csv")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(dict(response.items())['Content-Disposition'], r'attachment; filename="\w+.csv"')

    def test_export_csv_required_skills(self):
        """
        test GET /projects/export_csv_required-skills
        """
        url = reverse("project-export-csv-required-skills")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(dict(response.items())['Content-Disposition'], r'attachment; filename="\w+.csv"')

    def test_export_csv_suggested_students(self):
        """
        test GET /projects/export_csv_suggested-students
        """
        url = reverse("project-export-csv-suggested-students")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(dict(response.items())['Content-Disposition'], r'attachment; filename="\w+.csv"')
