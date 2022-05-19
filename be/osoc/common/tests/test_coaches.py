"""
Integration tests for coach API endpoints.

each test simulates an API call to one endpoint and checks if the response data and status code are correct
these tests test serializers.py and views.py and the API endpoints as a whole
"""
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import AdminFactory, CoachFactory
from osoc.common.models import Coach


class CoachTestsCoach(APITestCase):
    """
    test class for testing coach model by coach user (not all permissions)
    """
    def setUp(self):
        """
        test setup
        """
        CoachFactory()
        self.user = CoachFactory(email="coach2@example.com")
        self.client.force_authenticate(self.user)

    def test_get_coach_list_forbidden(self):
        """
        test GET /coaches/ without permission
        """
        url = reverse("coach-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coach_instance_forbidden(self):
        """
        test GET /coaches/{id}/ without permission
        """
        coach = Coach.objects.exclude(id=self.user.id).first()
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coach_instance_not_found(self):
        """
        test GET /coaches/{id}/ with non-existing id
        """
        url = reverse("coach-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_coach_instance_owner(self):
        """
        test GET /coaches/{id}/ while logged in as that user
        """
        coach = self.user
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], coach.email)

    def test_update_coach_forbidden(self):
        """
        test PUT /coaches/{id}/ without permission
        """
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
        """
        test PUT /coaches/{id}/ while logged in as that user
        """
        coach = self.user
        url = reverse("coach-detail", args=(coach.id,))
        data = {
            "first_name": "new first name",
            "last_name": "last name",
            "email": "email@example.com"
        }
        response = self.client.put(url, data=data, format="json")
        coach = Coach.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])
        # Is it possible to update 'coach' variable with latest info from database?
        self.assertEqual(coach.first_name, data["first_name"])

    def test_delete_coach_forbidden(self):
        """
        test DELETE /coaches/{id}/ without permission
        """
        coach = Coach.objects.first()
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_all_forbidden(self):
        """
        test DELETE /coaches/delete_all without permission
        """
        url = reverse("coach-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_export_csv_forbidden(self):
        """
        test GET /coaches/export_csv without permission
        """
        url = reverse("coach-export-csv")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CoachTestsAdmin(APITestCase):
    """
    test class for testing coach model by admin user (all permissions)
    """
    def setUp(self):
        """
        test setup
        """
        CoachFactory()
        self.admin = AdminFactory(email="admin@example.com")
        self.client.force_authenticate(self.admin)

    def test_get_coach_list(self):
        """
        test GET /coaches/
        """
        url = reverse("coach-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Coach.objects.count())

    def test_get_coach_instance(self):
        """
        test GET /coaches/{id}/
        """
        coach = Coach.objects.exclude(id=self.admin.id).first()
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_coach(self):
        """
        test DELETE /coaches/{id}/
        """
        coach = Coach.objects.first()
        url = reverse("coach-detail", args=(coach.id,))
        before_count = Coach.objects.count()
        response = self.client.delete(url)
        after_count = Coach.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_coach_not_found(self):
        """
        test GET /coaches/{id}/ with non-existing id
        """
        url = reverse("coach-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_self_forbidden(self):
        """
        test DELETE /coaches/{id}/ while logged in as that user
        """
        coach = self.admin
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_coach_update_status(self):
        """
        test PUT /coaches/{id}/update_status
        """
        coach = Coach.objects.exclude(id=self.admin.id).first()
        coach.is_admin = False
        coach.is_active = False
        coach.save()
        url = reverse("coach-update-status", args=(coach.id,))
        response = self.client.put(url, {"is_admin": True, "is_active": True}, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Coach.objects.get(id=coach.id).is_admin, True)
        self.assertEqual(Coach.objects.get(id=coach.id).is_active, True)

    def test_update_status_self_forbidden(self):
        """
        test PUT /coaches/{id}/update_status while logged in as that user
        """
        coach = self.admin
        url = reverse("coach-update-status", args=(coach.id,))
        response = self.client.put(url, {"is_admin": True, "is_active": True}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_status_bad_request(self):
        """
        test PUT /coaches/{id}/update_status whit bad request
        """
        coach = Coach.objects.first()
        url = reverse("coach-update-status", args=(coach.id,))
        response = self.client.put(url, {"is_admin": "not a boolean"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_coach(self):
        """
        test PUT /coaches/{id}/
        """
        coach = Coach.objects.get(email="coach@example.com")
        url = reverse("coach-detail", args=(coach.id,))
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "coach@example.com"
        }
        response = self.client.put(url, data=data, format="json")
        coach = Coach.objects.get(email="coach@example.com")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])
        # Is it possible to update 'coach' variable with latest info from database?
        self.assertEqual(coach.first_name, data["first_name"])

    def test_delete_all(self):
        """
        test DELETE /coaches/delete_all
        """
        url = reverse("coach-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Coach.objects.filter(is_admin=False).count(), 0)

    def test_export_csv(self):
        """
        test GET /coaches/export_csv
        """
        url = reverse("coach-export-csv")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(dict(response.items())['Content-Disposition'], r'attachment; filename="\w+.zip"')