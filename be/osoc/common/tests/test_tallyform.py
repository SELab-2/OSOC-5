"""
Unit tests for tally.py
"""
from django.test import TestCase
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
        tallyForm = TallyForm({})
        with self.assertRaisesMessage(ValueError, "Format error: Event type should be 'FORM_RESPONSE'."):
            tallyForm.validate({})
        with self.assertRaisesMessage(ValueError, "Format error: No fields (root > data > fields)."):
            tallyForm.validate({ "eventType": "FORM_RESPONSE" })

    def test_validation_question_error(self):
        """
        test question errors
        """
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

    def test_validation_skip_questions(self):
        """
        test skip questions
        """
        # Skip question 2 and 3 if answer for question 1 is "Backend development"
        self.questions[1]["answers"][0]["skip"] = [2, 3]
        tallyForm = TallyForm(self.questions)
        form = { "eventType": "FORM_RESPONSE", "data": { "fields": [
            { "key": "question_mRoXgd", "label": "What do/did you study?", "type": "CHECKBOXES", "value": [ "abc" ], "options": [ { "id": "abc", "text": "Backend development" } ] }
            ] } }
        self.assertEqual(tallyForm.validate(form), form)

    def test_transform_other_question(self):
        """
        test transform questions
        """
        # Skip question 2 and 3 if answer for question 1 is "Other"
        self.questions[1]["answers"][2]["skip"] = [2, 3]
        tallyForm = TallyForm(self.questions)
        form = { "eventType": "FORM_RESPONSE", "data": { "fields": [
            { "key": "question_mRoXgd", "label": "What do/did you study?", "type": "CHECKBOXES", "value": [ "abc" ], "options": [ { "id": "abc", "text": "Other" } ] },
            { "key": "question_mRfOpr", "label": "What do/did you study?", "type": "INPUT_TEXT", "value": "Bioinformatics" } ] } }
        self.assertEqual(tallyForm.validate(form), form)
        transformed = tallyForm.transform(form)
        self.assertEqual(transformed.get("studies", []), ["Bioinformatics"])

    def test_validate_and_transform(self):
        """
        test validate and transform questions
        """
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
