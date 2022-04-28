"""
Django tests for API endpoints.

Running tests is different because the project uses Docker:

    1. Run all tests:
        `docker exec -it osoc-be python manage.py test`

    2. Run one test class:
        `docker exec -it osoc-be python manage.py test osoc.common.tests.tests:<TESTCLASS>`

    3. Run a single test:
        `docker exec -it osoc-be python manage.py test osoc.common.tests.tests:<TESTCLASS>.<TESTMETHOD>`
"""
import json
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.test import TestCase
from osoc.common.tally.tally import TallyForm
from osoc.common.models import Coach, Project, ProjectSuggestion, SentEmail, Skill, Student, Suggestion
from osoc.common.utils import strip_and_lower_email


class UtilityTestCases(TestCase):
    def test_strip_and_lower_email(self):
        correct_email = 'admin@example.com'
        test_email = strip_and_lower_email('  Admin@Example.com    ')
        self.assertEqual(correct_email, test_email)

    def testGetNested(self):
        self.assertEqual(None, utils.getNested({'a': {'b': True}}, None, 'a', 'c'))
        self.assertEqual(None, utils.getNested({'a': {'b': True}}, None, 'b', 'a'))
        self.assertEqual(True, utils.getNested({'a': {'b': True }}, None, 'a', 'b'))
        self.assertEqual(True, utils.getNested({'a': {'b': { 'c': True }}}, None, 'a', 'b', 'c'))

class TallyFormTestCases(TestCase):
    def setUp(self):
       self.questions = {
            1: {
                "question": [ "What do/did you study?" ],
                "field": "studies",
                "type": "CHECKBOXES",
                "answers": [
                        { "answer": "Backend development" },
                        { "answer": "Business management" },
                        { "answer": "Other", "value": {
                            "question": [ "What do/did you study?" ],
                            "type": "INPUT_TEXT"
                            } } ],
                "required": True
            },
            2: {
                "question": [ "Are you a student?" ],
                "field": "student",
                "type": "MULTIPLE_CHOICE",
                "answers": [
                        { "answer": "Yes", "value": True, },
                        { "answer": "No", "value": False } ],
                "required": True
            },
            3: {
                "question": [ "Birth name" ],
                "field": "first_name",
                "type": "INPUT_TEXT",
                "required": True
            },
       }

    def testValidationFormatError(self):
        tallyForm = TallyForm({})
        with self.assertRaisesMessage(ValueError, "Format error: Event type should be 'FORM_RESPONSE'."):
            tallyForm.validate({})
        with self.assertRaisesMessage(ValueError, "Format error: No fields (root > data > fields)."):
            tallyForm.validate({ "eventType": "FORM_RESPONSE" })

    def testValidationQuestionError(self):
        self.questions[1]["required"] = False
        self.questions[2]["required"] = False
        tallyForm = TallyForm(self.questions)
        with self.assertRaisesMessage(ValueError, "Question is required"):
            tallyForm.validate({ "eventType": "FORM_RESPONSE", "data": { "fields": [
                { "key": "question_mRoXgd", "label": "Birth name", "type": "INPUT_TEXT", "value": None }
                ] } })
        with self.assertRaisesMessage(ValueError, "Missing question in form"):
            tallyForm.validate({ "eventType": "FORM_RESPONSE", "data": { "fields": [] } } )
        self.questions[2]["required"] = True
        self.questions[3]["required"] = False
        self.questions[2]["answers"] = []
        with self.assertRaisesMessage(ValueError, "Question has no answer"):
            tallyForm.validate({ "eventType": "FORM_RESPONSE", "data": { "fields": [
                { "key": "question_mRoXgd", "label": "Are you a student?", "type": "MULTIPLE_CHOICE", "value": "abc", "options": [ { "id": "abc", "text": "Yes" } ] }
                ] } } )

    def testValidationSkipQuestions(self):
        # Skip question 2 and 3 if answer for question 1 is "Backend development"
        self.questions[1]["answers"][0]["skip"] = [2, 3]
        tallyForm = TallyForm(self.questions)
        form = { "eventType": "FORM_RESPONSE", "data": { "fields": [
            { "key": "question_mRoXgd", "label": "What do/did you study?", "type": "CHECKBOXES", "value": [ "abc" ], "options": [ { "id": "abc", "text": "Backend development" } ] }
            ] } }
        self.assertEqual(tallyForm.validate(form), form)

    def testTransformOtherQuestion(self):
        # Skip question 2 and 3 if answer for question 1 is "Other"
        self.questions[1]["answers"][2]["skip"] = [2, 3]
        tallyForm = TallyForm(self.questions)
        form = { "eventType": "FORM_RESPONSE", "data": { "fields": [
            { "key": "question_mRoXgd", "label": "What do/did you study?", "type": "CHECKBOXES", "value": [ "abc" ], "options": [ { "id": "abc", "text": "Other" } ] },
            { "key": "question_mRfOpr", "label": "What do/did you study?", "type": "INPUT_TEXT", "value": "Bioinformatics" } ] } }
        self.assertEqual(tallyForm.validate(form), form)
        transformed = tallyForm.transform(form)
        self.assertEqual(transformed.get("studies", []), ["Bioinformatics"])

    def testValidateAndTransform(self):
        tallyForm = TallyForm(self.questions)
        form = { "eventType": "FORM_RESPONSE", "data": { "fields": [
            { "key": "question_mRoXgd", "label": "What do/did you study?", "type": "CHECKBOXES", "value": [ "a", "b", "c" ], "options": [
                { "id": "a", "text": "Backend development" },
                { "id": "b", "text": "Business management" },
                { "id": "c", "text": "Other" }
                ] },
            { "key": "question_mRfZds", "label": "What do/did you study?", "type": "INPUT_TEXT", "value": "Bioinformatics" },
            { "key": "question_mRoXgd", "label": "Are you a student?", "type": "MULTIPLE_CHOICE", "value": "a", "options": [ { "id": "a", "text": "Yes" } ] },
            { "key": "question_mRfLrs", "label": "Birth name", "type": "INPUT_TEXT", "value": "Henri" },
            ] } }
        self.assertEqual(tallyForm.validate(form), form)
        transformed = tallyForm.transform(form)
        self.assertEqual(transformed, {
            "first_name": "Henri",
            "student": True,
            "studies": [ "Backend development", "Business management", "Bioinformatics" ]
            })

class StudentTestsCoach(APITestCase):
    def setUp(self) -> None:
        student = Student.objects.create(
            first_name="First name",
            last_name="Last name",
            call_name="call name",
            email="example@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )
        skill = Skill.objects.create(
            name="skill",
            color="blue"
        )
        student.skills.add(skill)

        user = Coach.objects.create_user(
            first_name="username",
            last_name="last_name",
            email="email@example.com",
            password="Pas$w0rd"
        )
        self.client.force_authenticate(user)

    def test_get_student_list(self):
        url = reverse("student-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Student.objects.count())

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
        student = Student.objects.first()
        url = reverse("student-detail", args=(student.id,))
        before_count = Student.objects.count()
        response = self.client.delete(url)
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_student_not_found(self):
        url = reverse("student-detail", args=(50,))
        before_count = Student.objects.count()
        response = self.client.delete(url)
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(before_count, after_count)

    def test_create_student(self):
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
        url = reverse("student-list")
        before_count = Student.objects.count()
        response = self.client.post(url, {}, format="json")
        after_count = Student.objects.count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(before_count, after_count)

    def test_update_student(self):
        student = Student.objects.first()
        url = reverse("student-detail", args=(student.id,))
        student_data = json.loads(self.client.get(url, format="json").content)
        student_data["first_name"] = "new name"
        response = self.client.put(url, student_data, format="json")
        student = Student.objects.get(id=student.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(student.first_name, student_data["first_name"])

    def test_student_make_suggestion(self):
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
        student = Student.objects.first()
        url = reverse("student-make-suggestion", args=(student.id,))
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.post(url, {}, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(before_count, after_count)

    def test_student_remove_suggestion(self):
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
        student = Student.objects.first()
        student.suggestions.all().delete()
        url = reverse("student-remove-suggestion", args=(student.id,))
        before_count = Suggestion.objects.filter(student=student).count()
        response = self.client.delete(url, format="json")
        after_count = Suggestion.objects.filter(student=student).count()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(before_count, after_count)

    def test_student_make_final_decision_forbidden(self):
        student = Student.objects.first()
        url = reverse("student-make-final-decision", args=(student.id,))
        data = {
            "suggestion": "0",
            "reason": "a reason"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudentTestsAdmin(APITestCase):
    def setUp(self) -> None:
        Student.objects.create(
            first_name="First name",
            last_name="Last name",
            call_name="call name",
            email="example@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )

        admin = Coach.objects.create_user(
            first_name="admin",
            last_name="last_name",
            email="admin@example.com",
            password="Pas$w0rd",
            is_admin=True
        )
        self.client.force_authenticate(admin)

    def test_student_make_final_decision(self):
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

    def test_student_remove_final_decision(self):
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


class CoachTestsCoach(APITestCase):
    def setUp(self):
        Coach.objects.create(
            first_name="first name",
            last_name="last name",
            email="email2@example.com",
            password="p4ssWorD"
        )

        self.user = Coach.objects.create_user(
            first_name="username",
            last_name="last_name",
            email="email@example.com",
            password="Pas$w0rd"
        )
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

    def test_get_coach_instance_not_found(self):
        url = reverse("coach-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        coach = Coach.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])
        # Is it possible to update 'coach' variable with latest info from database?
        self.assertEqual(coach.first_name, data["first_name"])

    def test_delete_coach_forbidden(self):
        coach = Coach.objects.first()
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CoachTestsAdmin(APITestCase):
    def setUp(self):
        Coach.objects.create(
            first_name="first name",
            last_name="last name",
            password="p4ssWorD",
            email="email@example.com"
        )

        self.admin = Coach.objects.create_user(
            first_name="admin",
            password="Pas$w0rd",
            last_name="last_name",
            email="admin@example.com",
            is_admin=True
        )
        self.client.force_authenticate(self.admin)

    def test_get_coach_list(self):
        url = reverse("coach-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Coach.objects.count())

    def test_get_coach_instance(self):
        coach = Coach.objects.exclude(id=self.admin.id).first()
        url = reverse("coach-detail", args=(coach.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_coach(self):
        coach = Coach.objects.first()
        url = reverse("coach-detail", args=(coach.id,))
        before_count = Coach.objects.count()
        response = self.client.delete(url)
        after_count = Coach.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_coach_not_found(self):
        url = reverse("coach-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_coach_update_status(self):
        coach = Coach.objects.exclude(id=self.admin.id).first()
        coach.is_admin = False
        coach.is_active = False
        coach.save()
        url = reverse("coach-update-status", args=(coach.id,))
        response = self.client.put(url, {"is_admin": True, "is_active": True})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Coach.objects.get(id=coach.id).is_admin, True)
        self.assertEqual(Coach.objects.get(id=coach.id).is_active, True)

    def test_update_coach(self):
        coach = Coach.objects.get(email="email@example.com")
        url = reverse("coach-detail", args=(coach.id,))
        data = {
            "first_name": "new first name",
            "last_name": "last name",
            "email": "email@example.com"
        }
        response = self.client.put(url, data=data, format="json")
        coach = Coach.objects.get(email="email@example.com")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])
        # Is it possible to update 'coach' variable with latest info from database?
        self.assertEqual(coach.first_name, data["first_name"])


class ProjectTestsCoach(APITestCase):
    def setUp(self) -> None:
        skill = Skill.objects.create(
            name="skill",
            color="blue"
        )
        project1 = Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info",
        )
        project1.required_skills.add(skill)
        project2 = Project.objects.create(
            name="Test_2",
            partner_name="Partner",
            extra_info="Exra info",
        )
        project2.required_skills.add(skill)
        Student.objects.create(
            first_name="First name",
            last_name="Last name",
            call_name="call name",
            email="example@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )

        self.user = Coach.objects.create_user(
            first_name="username",
            last_name="last_name",
            email="email@example.com",
            password="Pas$w0rd")
        self.client.force_authenticate(self.user)

    def test_get_project_list(self):
        url = reverse("project-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Project.objects.count())

    def test_get_project_instance(self):
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], project.name)

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
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_project_forbidden(self):
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_suggest_student(self):
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

    def test_project_suggest_student_bad_request(self):
        project = Project.objects.first()
        url = reverse("project-suggest-student", args=(project.id,))
        student = Student.objects.first()
        skill = Skill.objects.create(
            name="skill2",
            color="green"
        )
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

    def test_project_remove_student(self):
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

    def test_project_get_conflicting(self):
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

        self.assertEqual(len(response.data["conflicts"]), 1)


class ProjectTestsAdmin(APITestCase):
    def setUp(self) -> None:
        Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info"
        )
        Skill.objects.create(
            name="skill",
            color="blue"
        )

        admin = Coach.objects.create_user(
            first_name="admin",
            password="Pas$w0rd",
            last_name="last_name",
            email="admin@example.com",
            is_admin=True
        )
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
        project = Project.objects.first()
        url = reverse("project-detail", args=(project.id,))
        before_count = Project.objects.count()
        response = self.client.delete(url)
        after_count = Project.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_project_not_found(self):
        url = reverse("project-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project(self):
        project = Project.objects.first()
        skill = Skill.objects.create(
            name="skill2",
            color="green"
        )
        coach = Coach.objects.create_user(
            first_name="coach",
            password="Pas$w0rd",
            last_name="last_name",
            email="coach@example.com"
        )
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

        # its the same but different url, uncomment this to check
        # project_data = json.loads(self.client.get(reverse("project-detail", args=(project.id,))).content)
        # self.assertEqual(project_data["required_skills"], data["required_skills"])


class SkillTestsCoach(APITestCase):
    def setUp(self):
        Skill.objects.create(
            name="skill",
            color="blue"
        )
        Skill.objects.create(
            name="skill_2",
            color="red"
        )

        user = Coach.objects.create_user(
            first_name="username",
            password="Pas$w0rd",
            last_name="last_name",
            email="email@example.com"
        )
        self.client.force_authenticate(user)

    def test_get_skill_list(self):
        url = reverse("skill-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Skill.objects.count())

    def test_get_skill_instance(self):
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], skill.name)

    def test_get_skill_instance_not_found(self):
        url = reverse("skill-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_skill(self):
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
        url = reverse("skill-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_skill(self):
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
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SkillTestsAdmin(APITestCase):
    def setUp(self):
        Skill.objects.create(
            name="skill",
            color="blue"
        )
        Skill.objects.create(
            name="skill_2",
            color="red"
        )

        self.admin = Coach.objects.create_user(
            first_name="username",
            password="Pas$w0rd",
            last_name="last_name",
            email="email@example.com",
            is_admin=True
        )
        self.client.force_authenticate(self.admin)

    def test_delete_skill_not_used(self):
        skill = Skill.objects.first()
        url = reverse("skill-detail", args=(skill.id,))
        before_count = Skill.objects.count()
        response = self.client.delete(url)
        after_count = Skill.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_skill_used(self):
        skill = Skill.objects.first()
        project = Project.objects.create(
            name="Test",
            partner_name="Partner",
            extra_info="Extra info"
        )
        # add skill to project such that a projectsuggestion can be made
        project.required_skills.add(skill)
        student = Student.objects.create(
            first_name="First name",
            last_name="Last name",
            call_name="call name",
            email="example@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )
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
        url = reverse("skill-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SentEmailTests(APITestCase):
    def setUp(self):
        student = Student.objects.create(
            first_name="First name",
            last_name="Last name",
            call_name="call name",
            email="example@example.com",
            phone_number="+14255550123",
            language="dutch",
            cv="https://example.com",
            portfolio="https://example.com",
            school_name="Example",
            degree="Example",
            studies="Example",
            alum=False,
            employment_agreement="test value",
            english_rating=2,
            motivation="test value",
            fun_fact="test value",
            degree_duration=2,
            degree_current_year=1,
            best_skill="test value"
        )
        user = Coach.objects.create_user(
            first_name="username",
            password="Pas$w0rd",
            last_name="last_name",
            email="email@example.com"
        )
        self.client.force_authenticate(user)
        SentEmail.objects.create(
            sender=user,
            receiver=student,
            info="email info"
        )

    def test_get_email_list(self):
        url = reverse("sentemail-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), SentEmail.objects.count())

    def test_get_email_instance(self):
        email = SentEmail.objects.first()
        url = reverse("sentemail-detail", args=(email.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], email.id)

    def test_get_email_instance_not_found(self):
        url = reverse("sentemail-detail", args=(50,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_email(self):
        email = SentEmail.objects.first()
        url = reverse("sentemail-detail", args=(email.id,))
        before_count = SentEmail.objects.count()
        response = self.client.delete(url)
        after_count = SentEmail.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(before_count, after_count+1)

    def test_delete_email_not_found(self):
        url = reverse("sentemail-detail", args=(50,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_email(self):
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
        url = reverse("sentemail-list")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_email(self):
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
