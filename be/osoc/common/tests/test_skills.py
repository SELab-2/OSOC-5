"""
Integration tests for skill API endpoints.

each test simulates an API call to one endpoint and checks if the response data and status code are correct
these tests test serializers.py and views.py and the API endpoints as a whole
"""
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import AdminFactory, CoachFactory, ProjectFactory, SkillFactory, StudentFactory
from osoc.common.models import ProjectSuggestion, Skill


class SkillTestsCoach(APITestCase):
    """
    test class for testing skill model by coach user (not all permissions)
    """
    def setUp(self):
        """
        test setup
        """
        SkillFactory()
        SkillFactory(name="skill2")
        user = CoachFactory()
        self.client.force_authenticate(user)

    def test_get_skill_list(self):
        """
        test GET /skills/
        """
        url = reverse("skill-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Skill.objects.count())

    def test_get_skill_instance(self):
        """
        test GET /skills/{id}/
        """
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], skill.name)

    def test_get_skill_instance_not_found(self):
        """
        test GET /skills/{id}/ with non-existing id
        """
        url = reverse("skill-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_skill(self):
        """
        test POST /skills/
        """
        data = {
            "name": "skill_3",
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
        """
        test POST /skills/ with a bad request
        """
        url = reverse("skill-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_skill(self):
        """
        test PUT /skills/{id}/
        """
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        data = {
            "name": "new name",
            "color": "new color"
        }
        response = self.client.put(url, data, format="json")
        skill = Skill.objects.get(id=skill.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(skill.name, data["name"])

    def test_delete_forbidden(self):
        """
        test DELETE /skills/{id}/ without permission
        """
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_all_forbidden(self):
        """
        test DELETE /skills/delete_all without permission
        """
        url = reverse("skill-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_export_csv_forbidden(self):
        """
        test GET /skills/export_csv without permission
        """
        url = reverse("skill-export-csv")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SkillTestsAdmin(APITestCase):
    """
    test class for testing skill model by admin user (all permissions)
    """
    def setUp(self):
        """
        test setup
        """
        SkillFactory()
        SkillFactory(name="skill2")
        self.admin = AdminFactory()
        self.client.force_authenticate(self.admin)

    def test_delete_skill_not_used(self):
        """
        test DELETE /skills/{id}/
        """
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        before_count = Skill.objects.count()
        response = self.client.delete(url)
        after_count = Skill.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_skill_used(self):
        """
        test DELETE /skills/{id}/ that is used in a project
        """
        skill = Skill.objects.first()
        project = ProjectFactory()
        # add skill to project such that a projectsuggestion can be made
        project.required_skills.add(skill)
        student = StudentFactory()
        # add student to projectsuggestions, now the skill is "used" in this project
        ProjectSuggestion.objects.create(
            project=project,
            student=student,
            skill=skill,
            coach=self.admin
        )

        url = reverse("skill-detail", args=(skill.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_skill_not_found(self):
        """
        test DELETE /skills/{id}/ with non-existing id
        """
        url = reverse("skill-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all(self):
        """
        test DELETE /skills/delete_all
        """
        url = reverse("skill-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.count(), 0)

    def test_delete_all_some_used(self):
        """
        test DELETE /skills/delete_all while some skills are used in a projectsuggestion
        """
        skill = SkillFactory(name="used skill")
        project = ProjectFactory()
        # add skill to project such that a projectsuggestion can be made
        project.required_skills.add(skill)
        student = StudentFactory()
        # add student to projectsuggestions, now the skill is "used" in this project
        # pylint: disable=duplicate-code
        ProjectSuggestion.objects.create(
            project=project,
            student=student,
            skill=skill,
            coach=self.admin
        )
        url = reverse("skill-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Skill.objects.count(), 1)

    def test_export_csv(self):
        """
        test GET /skills/export_csv
        """
        url = reverse("skill-export-csv")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(dict(response.items())['Content-Disposition'], r'attachment; filename="\w+.zip"')
