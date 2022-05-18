"""
Integration tests for sentemail API endpoints.

each test simulates an API call to one endpoint and checks if the response data and status code are correct
these tests test serializers.py and views.py and the API endpoints as a whole
"""
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import AdminFactory, CoachFactory, SentEmailFactory, StudentFactory
from osoc.common.models import Coach, SentEmail, Student

class SentEmailTestsCoach(APITestCase):
    """
    test class for testing sentemail model
    """
    def setUp(self):
        """
        test setup
        """
        student = StudentFactory()
        user = CoachFactory()
        self.client.force_authenticate(user)
        SentEmailFactory(sender=user, receiver=student)

    def test_get_email_list(self):
        """
        test GET /sentemails/
        """
        url = reverse("sentemail-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], SentEmail.objects.count())

    def test_get_email_instance(self):
        """
        test GET /sentemails/{id}/
        """
        email = SentEmail.objects.first()
        url = reverse("sentemail-detail", args=(email.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], email.id)

    def test_get_email_instance_not_found(self):
        """
        test GET /sentemails/{id}/ with non-exisiting id
        """
        url = reverse("sentemail-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_email(self):
        """
        test DELETE /sentemails/{id}/
        """
        email = SentEmail.objects.first()
        url = reverse("sentemail-detail", args=(email.id,))
        before_count = SentEmail.objects.count()
        response = self.client.delete(url)
        after_count = SentEmail.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_email_not_found(self):
        """
        test DELETE /sentemails/{id}/ with non-exisiting id
        """
        url = reverse("sentemail-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_email(self):
        """
        test POST /sentemails/
        """
        student = Student.objects.first()
        coach = Coach.objects.first()
        data = {
            "sender": reverse("coach-detail", args=(coach.id,)),
            "receiver": reverse("student-detail", args=(student.id,)),
            "info": "info about this email"
        }
        url = reverse("sentemail-list")
        before_count = SentEmail.objects.count()
        response = self.client.post(url, data, format="json")
        after_count = SentEmail.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["info"], data["info"])
        self.assertEqual(before_count, after_count-1)

    def test_create_email_bad_request(self):
        """
        test POST /sentemails/ with a bad request
        """
        url = reverse("sentemail-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_email(self):
        """
        test PUT /sentemails/{id}
        """
        email = SentEmail.objects.first()
        student = Student.objects.first()
        coach = Coach.objects.first()
        url = reverse("sentemail-detail", args=(email.id,))
        data = {
            "sender": reverse("coach-detail", args=(coach.id,)),
            "receiver": reverse("student-detail", args=(student.id,)),
            "info": "new info"
        }
        response = self.client.put(url, data, format="json")
        email = SentEmail.objects.get(id=email.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(email.info, data["info"])

    def test_delete_all_forbidden(self):
        """
        test DELETE /sentemails/delete_all without permission
        """
        url = reverse("sentemail-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SentEmailTestsAdmin(APITestCase):
    """
    test class for testing sentemail model by admin user (all permissions)
    """
    def setUp(self):
        """
        test setup
        """
        student = StudentFactory()
        admin = AdminFactory()
        self.client.force_authenticate(admin)
        SentEmailFactory(sender=admin, receiver=student)

    def test_delete_all(self):
        """
        test DELETE /sentemails/delete_all
        """
        url = reverse("sentemail-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SentEmail.objects.count(), 0)

