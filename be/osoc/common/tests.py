from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from osoc.common.models import Coach, Project, Skill, Student


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

        user = Coach.objects.create_user(
            first_name="username", password="Pas$w0rd", last_name="last_name", email="email@example.com")
        self.client.force_authenticate(user)

    def test_get_project_list(self):
        url = reverse("project-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Project.objects.count())
    
    def test_get_project_instance(self):
        id = Project.objects.first().id
        url = reverse("project-detail", args=(id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test")
        self.assertEqual(response.data["partner_name"], "Partner")
        self.assertEqual(response.data["extra_info"], "Extra info")
    
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


class ProjectTestsAdmin(APITestCase):
    def setUp(self) -> None:
        Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info"
        )
        Skill.objects.create(
            name="skill",
            description="a skill"
        )

        admin = Coach.objects.create_user(
            first_name="admin", password="Pas$w0rd", last_name="last_name", email="admin@example.com", is_admin=True)
        self.client.force_authenticate(admin)

    def test_create_project(self):
        data = {
            "name": "Test_2",
            "partner_name": "Partner",
            "extra_info": "Extra info",
            "required_skills": [{"skill": "/skills/1/", "amount": "2"}],
            "coaches": ["/coaches/1/"]
        }
        url = reverse("project-list")
        before_count = Project.objects.count()
        response = self.client.post(url, data, format="json")
        after_count = Project.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Test_2")
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




# class SkillTests(APITestCase):
#     def setUp(self):
#         Skill.objects.create(
#             name="Skill",
#             description="A skill"
#         )

#         user = Coach.objects.create_user(
#             first_name="username", password="Pas$w0rd", last_name="last_name", email="email@example.com")
#         self.client.force_authenticate(user)

#     def test_get_all_skills(self):
#         response = self.client.get("/skills/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.data["results"][0]
#         self.assertEqual(data["name"], "Skill")
#         self.assertEqual(data["description"], "A skill")

#     def test_get_single_skill(self):
#         response = self.client.get("/skills/2/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         data = response.data
#         self.assertEqual(data["name"], "Skill")
#         self.assertEqual(data["description"], "A skill")

#     def test_remove_skill(self):
#         response = self.client.delete("/skills/3/")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         response = self.client.get("/skills/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 0)


# class StudentTests(APITestCase):
#     def setUp(self) -> None:
#         Student.objects.create(
#             first_name="First name",
#             last_name="Last name",
#             email="example@example.com",
#             cv="https://example.com",
#             portfolio="https://example.com",
#             school_name="Example",
#             degree="Example",
#             studies="Example"
#         )

#         user = Coach.objects.create_user(
#             first_name="username", password="Pas$w0rd", last_name="last_name", email="email@example.com")
#         self.client.force_authenticate(user)

#     def test_get_single_student(self):
#         response = self.client.get("/students/1/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.data
#         self.assertEqual(data["email"], "example@example.com")

#     def test_make_erroneous_suggestion(self):
#         response = self.client.post(
#             "/students/1/make_suggestion/")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     # def test_make_suggestion(self):
#     #     TODO: {"detail": ErrorDetail(string="Not found.", code="not_found")}
#     #     response = self.client.post(
#     #         "/students/1/make_suggestion/",
#     #         {"suggestion": 0, "coach": "/coaches/7/"})
#     #     print(response)
#     #     print(response.data)
