from rest_framework.test import APITestCase
from rest_framework import status

from osoc.common.models import Coach, Project, Skill, Student


class Projects(APITestCase):
    def setUp(self) -> None:
        Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info"
        )

        user = Coach.objects.create_user(
            first_name='username', password='Pas$w0rd', last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

    def test_get_all_projects(self):
        response = self.client.get("/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'][0]
        self.assertEqual(data["name"], "Test")
        self.assertEqual(data["partner_name"], "Partner")
        self.assertEqual(data["extra_info"], "Extra info")


class Skills(APITestCase):
    def setUp(self):
        Skill.objects.create(
            name="Skill",
            description="A skill"
        )

        user = Coach.objects.create_user(
            first_name='username', password='Pas$w0rd', last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

    def test_get_all_skills(self):
        response = self.client.get('/skills/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'][0]
        self.assertEqual(data["name"], "Skill")
        self.assertEqual(data["description"], "A skill")

    def test_get_single_skill(self):
        response = self.client.get('/skills/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["name"], "Skill")
        self.assertEqual(data["description"], "A skill")

    def test_remove_skill(self):
        response = self.client.delete("/skills/3/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get("/skills/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class Students(APITestCase):
    def setUp(self) -> None:
        Student.objects.create(
            first_name="First name",
            last_name="Last name",
            email="example@example.com",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example"
        )

        user = Coach.objects.create_user(
            first_name='username', password='Pas$w0rd', last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

    def test_get_single_student(self):
        response = self.client.get('/students/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["email"], "example@example.com")

    def test_make_erroneous_suggestion(self):
        response = self.client.post(
            '/students/1/make_suggestion/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_make_suggestion(self):
    #     TODO: {'detail': ErrorDetail(string='Not found.', code='not_found')}
    #     response = self.client.post(
    #         '/students/1/make_suggestion/',
    #         {'suggestion': 0, 'coach': '/coaches/7/'})
    #     print(response)
    #     print(response.data)
