"""
Integration tests for API endpoints.
each test simulates an API call to one endpoint and checks if the response data and status code are correct
these tests test serializers.py and views.py and the API endpoints as a whole
"""
# pylint: disable=duplicate-code,too-many-lines
import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import AdminFactory, CoachFactory, ProjectFactory, SentEmailFactory, SkillFactory, StudentFactory
from osoc.common.models import Coach, Project, ProjectSuggestion, SentEmail, Skill, Student, Suggestion


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


class RegisterTests(APITestCase):
    """
    test class for testing register functionality
    """
    def setUp(self):
        """
        test setup
        """
        self.admin = AdminFactory()
        self.client.force_authenticate(self.admin)

    def test_register(self):
        """
        test POST /auth/register
        """
        url = reverse("register")
        data = {
            "email": "test.user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "password*&^%"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_passwords_dont_match(self):
        """
        test POST /auth/register with two different passwords
        """
        url = reverse("register")
        data = {
            "email": "test.user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "wrong"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_email_exists(self):
        """
        test POST /auth/register with an existing email
        """
        url = reverse("register")
        data = {
            "email": self.admin.email,
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "password*&^%"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    """
    test class for testing login functionality
    """
    def setUp(self):
        """
        test setup
        """
        admin = AdminFactory()
        self.client.force_authenticate(admin)
        # create user with register endpoint so that the password is hashed and can be used to log in
        self.user_data = {
            "email": "test.user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "password*&^%"
        }
        url = reverse("register")
        self.client.post(url, self.user_data, format="json")
        # set coach active to be able to log in
        coach = Coach.objects.get(email=self.user_data["email"])
        coach.is_active = True
        coach.save()

    def test_login(self):
        """
        test POST /api-auth/login/
        """
        url = reverse("rest_login")
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password1"]
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_doenst_exist(self):
        """
        test POST /api-auth/login/ with a non-existing user
        """
        url = reverse("rest_login")
        data = {
            "email": "non_existing_email",
            "password": "password"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        """
        test POST /api-auth/login/ with a wrong password
        """
        url = reverse("rest_login")
        data = {
            "email": self.user_data["email"],
            "password": "wrong_password"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_bad_request(self):
        """
        test POST /api-auth/login/ with data missing
        """
        url = reverse("rest_login")
        data = {
            "email": self.user_data["email"],
            "password": ""
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
