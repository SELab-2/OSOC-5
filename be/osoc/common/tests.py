from rest_framework.test import APITestCase
from rest_framework import status

from osoc.common.models import Coach, Project


class GetAllProjects(APITestCase):

    def setUp(self) -> None:
        Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info"
        )

    def test_get_all_projects(self):
        user = Coach.objects.create_user(
            first_name='username', password='Pas$w0rd', last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

        response = self.client.get("/projects", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'][0]
        self.assertEqual(data["name"], "Test")
        self.assertEqual(data["partner_name"], "Partner")
        self.assertEqual(data["extra_info"], "Extra info")
