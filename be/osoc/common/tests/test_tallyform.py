"""
Unit tests for tally.py
"""
# pylint: disable=duplicate-code,too-many-lines
import json
from pathlib import Path
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import SkillFactory
from osoc.common.tally.tally import TallyForm 


class TallyFormTestCases(TestCase):
    """
    test class for testing tally form methods
    """
    def setUp(self):
        """
        test setup
        """
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

    def test_validation_format_error(self):
        """
        test format error
        """
        tally_form = TallyForm({})
        with self.assertRaisesMessage(ValueError, "Format error: Event type should be 'FORM_RESPONSE'."):
            tally_form.validate({})
        with self.assertRaisesMessage(ValueError, "Format error: No fields (root > data > fields)."):
            tally_form.validate({ "eventType": "FORM_RESPONSE" })

    def test_validation_question_error(self):
        """
        test question errors
        """
        self.questions[1]["required"] = False
        self.questions[2]["required"] = False
        tally_form = TallyForm(self.questions)
        with self.assertRaisesMessage(ValueError, "Question is required"):
            tally_form.validate({ "eventType": "FORM_RESPONSE", "data": { "fields": [
                { "key": "question_mRoXgd", "label": "Birth name", "type": "INPUT_TEXT", "value": None }
                ] } })
        with self.assertRaisesMessage(ValueError, "Missing question in form"):
            tally_form.validate({ "eventType": "FORM_RESPONSE", "data": { "fields": [] } } )
        self.questions[2]["required"] = True
        self.questions[3]["required"] = False
        self.questions[2]["answers"] = []
        with self.assertRaisesMessage(ValueError, "Question has no answer"):
            tally_form.validate({ "eventType": "FORM_RESPONSE", "data": { "fields": [
                { "key": "question_mRoXgd", "label": "Are you a student?", "type": "MULTIPLE_CHOICE", "value": "abc", "options": [ { "id": "abc", "text": "Yes" } ] }
                ] } } )

    def test_validation_skip_questions(self):
        """
        test skip questions
        """
        # Skip question 2 and 3 if answer for question 1 is "Backend development"
        self.questions[1]["answers"][0]["skip"] = [2, 3]
        tally_form = TallyForm(self.questions)
        form = { "eventType": "FORM_RESPONSE", "data": { "fields": [
            { "key": "question_mRoXgd", "label": "What do/did you study?", "type": "CHECKBOXES", "value": [ "abc" ], "options": [ { "id": "abc", "text": "Backend development" } ] }
            ] } }
        self.assertEqual(tally_form.validate(form), form)

    def test_transform_other_question(self):
        """
        test transform questions
        """
        # Skip question 2 and 3 if answer for question 1 is "Other"
        self.questions[1]["answers"][2]["skip"] = [2, 3]
        tally_form = TallyForm(self.questions)
        form = { "eventType": "FORM_RESPONSE", "data": { "fields": [
            { "key": "question_mRoXgd", "label": "What do/did you study?", "type": "CHECKBOXES", "value": [ "abc" ], "options": [ { "id": "abc", "text": "Other" } ] },
            { "key": "question_mRfOpr", "label": "What do/did you study?", "type": "INPUT_TEXT", "value": "Bioinformatics" } ] } }
        self.assertEqual(tally_form.validate(form), form)
        transformed = tally_form.transform(form)
        self.assertEqual(transformed.get("studies", []), ["Bioinformatics"])

    def test_validate_and_transform(self):
        """
        test validate and transform questions
        """
        tally_form = TallyForm(self.questions)
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
        self.assertEqual(tally_form.validate(form), form)
        transformed = tally_form.transform(form)
        self.assertEqual(transformed, {
            "first_name": "Henri",
            "student": True,
            "studies": [ "Backend development", "Business management", "Bioinformatics" ]
            })


class TallyRegistrationTests(APITestCase):
    """
    tests class for testing the tally API endpoint used by the webhook
    """
    def setUp(self):
        """
        test setup
        """
        path = Path('osoc/common/tally/test_data.json')
        with open(path) as file:
            self.data = json.load(file)
        SkillFactory(name="Backend development")

    def test_tally_registration(self):
        """
        test POST /students/tallyregistration
        """
        url = reverse("student-tallyregistration")
        response = self.client.post(url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tally_registration_bad_request(self):
        """
        test POST /students/tallyregistration with a bad request
        """
        url = reverse("student-tallyregistration")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
