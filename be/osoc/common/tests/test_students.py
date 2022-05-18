"""
Integration tests for student API endpoints.

each test simulates an API call to one endpoint and checks if the response data and status code are correct
these tests test serializers.py and views.py and the API endpoints as a whole
"""
import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import AdminFactory, CoachFactory, SkillFactory, StudentFactory
from osoc.common.models import Skill, Student, Suggestion


class StudentTestsCoach(APITestCase):
    """
    test class for testing student model by coach user (not all permissions)
    """
    def setUp(self) -> None:
        """
        test setup
        """
        student = StudentFactory()
        skill = SkillFactory()
        student.skills.add(skill)
        user = CoachFactory()
        self.client.force_authenticate(user)

    def test_get_student_list(self):
        """
        test GET /students/
        """
        url = reverse("student-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Student.objects.count())

    def test_get_student_instance(self):
        """
        test GET /students/{id}/
        """
        student = Student.objects.first()
        url = reverse("student-detail", args=(student.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], student.email)

    def test_get_student_instance_not_found(self):
        """
        test GET /students/{id}/ with non-existing id
        """
        url = reverse("student-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_student(self):
        """
        test DELETE /students/{id}/
        """
        student = Student.objects.first()
        url = reverse("student-detail", args=(student.id,))
        before_count = Student.objects.count()
        response = self.client.delete(url)
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_student_not_found(self):
        """
        test DELETE /students/{id}/ with non-existing id
        """
        url = reverse("student-detail", args=(50,))
        before_count = Student.objects.count()
        response = self.client.delete(url)
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(before_count, after_count)

    def test_create_student(self):
        """
        test POST /students/
        """
        skill = Skill.objects.first()
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "cv": "https://example.com",
            "portfolio": "https://example.com",
            "school_name": "Example",
            "degree": "Example",
            "studies": "Example",
            "employment_agreement": "test_value",
            "language": "dutch",
            "english_rating": 2,
            "motivation": "test_value",
            "fun_fact": "test_value",
            "degree_duration": 5,
            "degree_current_year": 2,
            "best_skill": "test_value",
            "skills": [reverse("skill-detail", args=(skill.id,))]
        }
        url = reverse("student-list")
        before_count = Student.objects.count()
        response = self.client.post(url, data, format="json")
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(before_count, after_count-1)

    def test_create_student_bad_request(self):
        """
        test POST /students/ with bad request
        """
        url = reverse("student-list")
        before_count = Student.objects.count()
        response = self.client.post(url, {}, format="json")
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(before_count, after_count)

    def test_update_student(self):
        """
        test PUT /students/{id}/
        """
        student = Student.objects.first()
        url = reverse("student-detail", args=(student.id,))
        student_data = json.loads(self.client.get(url, format="json").content)
        student_data["first_name"] = "new name"
        response = self.client.put(url, student_data, format="json")
        student = Student.objects.get(id=student.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(student.first_name, student_data["first_name"])

    def test_student_make_suggestion(self):
        """
        test POST /students/{id}/make_suggestion
        """
        student = Student.objects.first()
        url = reverse("student-make-suggestion", args=(student.id,))
        data = {
            "suggestion": "0",
            "reason": "a reason"
        }
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.post(url, data, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count, after_count-1)

    def test_student_make_suggestion_bad_request(self):
        """
        test POST /students/{id}/make_suggestion with bad request
        """
        student = Student.objects.first()
        url = reverse("student-make-suggestion", args=(student.id,))
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.post(url, {}, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(before_count, after_count)

    def test_student_remove_suggestion(self):
        """
        test DELETE /students/{id}/remove_suggestion
        """
        student = Student.objects.first()
        # first, make sure there is a suggestion
        url = reverse("student-make-suggestion", args=(student.id,))
        data = {
            "suggestion": "0",
            "reason": "a reason"
        }
        self.client.post(url, data, format="json")

        url = reverse("student-remove-suggestion", args=(student.id,))
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.delete(url, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_student_remove_suggestion_not_found(self):
        """
        test DELETE /students/{id}/remove_suggestion without a suggestion
        """
        student = Student.objects.first()
        student.suggestions.all().delete()
        url = reverse("student-remove-suggestion", args=(student.id,))
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.delete(url, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(before_count, after_count)

    def test_student_make_final_decision_forbidden(self):
        """
        test POST /students/{id}/make_final_decision without permission
        """
        student = Student.objects.first()
        url = reverse("student-make-final-decision", args=(student.id,))
        data = {
            "suggestion": "0",
            "reason": "a reason"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_bulk_status(self):
        """
        test POST /students/bulk_status
        """
        student_status = '2'
        url = reverse("student-bulk-status")
        data = {
            "status": student_status,
            "students": [reverse("student-detail", args=(student.id,)) for student in Student.objects.all()]
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(student.status == student_status for student in Student.objects.all()))

    def test_student_bulk_status_bad_request(self):
        """
        test POST /students/bulk_status with bad request
        """
        url = reverse("student-bulk-status")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_all_forbidden(self):
        """
        test DELETE /students/delete_all without permission
        """
        url = reverse("student-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_students_count(self):
        """
        test GET /students/count
        """
        counts = {
            "yes": Student.objects.filter(final_decision__suggestion=Suggestion.Suggestion.YES).count(),
            "no": Student.objects.filter(final_decision__suggestion=Suggestion.Suggestion.NO).count(),
            "maybe": Student.objects.filter(final_decision__suggestion=Suggestion.Suggestion.MAYBE).count(),
            "undecided": Student.objects.filter(final_decision=None).count()
        }

        url = reverse("student-count")
        response = self.client.get(url)

        self.assertEqual(response.data['counts'], counts)


class StudentTestsAdmin(APITestCase):
    """
    test class for testing student model by admin user (all permissions)
    """
    def setUp(self) -> None:
        """
        test setup
        """
        StudentFactory()
        admin = AdminFactory()
        self.client.force_authenticate(admin)

    def test_student_make_final_decision(self):
        """
        test POST /students/{id}/make_final_decision
        """
        student = Student.objects.first()
        url = reverse("student-make-final-decision", args=(student.id,))
        data = {
            "suggestion": "0",
            "reason": "a reason"
        }
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.post(url, data, format="json")
        after_count = Suggestion.objects.filter(student=student).count()
        student = Student.objects.get(id=student.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(student.final_decision.suggestion, data["suggestion"])
        self.assertEqual(before_count, after_count-1)

    def test_student_make_final_decision_bad_request(self):
        """
        test POST /students/{id}/make_final_decision with bad request
        """
        student = Student.objects.first()
        url = reverse("student-make-final-decision", args=(student.id,))
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_remove_final_decision(self):
        """
        test DELETE /students/{id}/remove_final_decision
        """
        student = Student.objects.first()
        # first make sure there is a suggestion to delete
        url = reverse("student-make-final-decision", args=(student.id,))
        data = {
            "suggestion": "0",
            "reason": "a reason"
        }
        self.client.post(url, data, format="json")

        url = reverse("student-remove-final-decision", args=(student.id,))
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.delete(url, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_all(self):
        """
        test DELETE /students/delete_all
        """
        url = reverse("student-delete-all")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
