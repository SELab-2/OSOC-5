"""
Tally form (https://tally.so); method for students to register.
"""
import json
from ..utils import get_nested, assert_or_raise


class TallyForm:
    """
    Validate and manipulate student register form from Tally.
    """
    def __init__(self, questions):
        self.questions = questions

    @classmethod
    def from_file(cls, questionfile='osoc/common/tally/questions.json'):
        """
        load questions from a json file
        """
        with open(questionfile, 'r', encoding="utf-8") as file:
            questions = json.load(file)
        return cls(questions)

    def validate(self, form):
        """
        Validate Tally form; make sure all student data is present.
        """
        assert_or_raise(form.get("eventType", None) == "FORM_RESPONSE", "Format error: Event type should be 'FORM_RESPONSE'.")
        # Get question fields from form
        fields = get_nested(form, None, "data", "fields")
        assert_or_raise(fields is not None, "Format error: No fields (root > data > fields).")
        # Validate (required) questions
        skip_questions = []
        for i, question in self.questions.items():
            if not question["required"] or i in skip_questions:
                continue
            # Required questions should have matching fields in the form
            filtered_fields = self.find_fields(question, fields)
            assert_or_raise(filtered_fields, f"Missing question in form: {', '.join(question['question'])}.")
            # Required questions should have a value
            field_value = self.search_field_value(filtered_fields, question["type"])
            assert_or_raise(field_value is not None, f"Question is required: {', '.join(question['question'])}.")
            # Add skip values if necessary
            answer = self.get_question_answer(question, field_value, fields)
            assert_or_raise(answer is not None, f"Question has no answer: {', '.join(question['question'])}.")
            skip_questions.extend(answer.get("skip", []))
        return form

    def find_fields(self, question, fields):
        """
        Find fields that correspond with a given question.
        """
        found_fields = []
        for field in fields:
            if field["label"] in question["question"] and self.__equal(field["type"], question["type"]):
                found_fields.append(field)
        return found_fields

    def search_field_value(self, fields, qtype):
        """
        Search (filtered) fields for a value with a given type.
        """
        value = None
        i = 0
        while value is None and i < len(fields):
            value = self.get_field_value(fields[i], qtype)
            i += 1
        return value

    def get_field_value(self, field, qtype): # pylint: disable=no-self-use
        """
        Get value from field with the given type.
        """
        fval = None
        if qtype == "MULTIPLE_CHOICE":
            option_id = field["value"]
            for option in field["options"]:
                if option["id"] == option_id:
                    fval = option["text"]
                    break
        elif qtype == "CHECKBOXES":
            checked = field["value"]
            fval = []
            for option in field["options"]:
                if option["id"] in checked:
                    fval.append(option["text"])
        else:
            # Text as value
            fval = field["value"]
        return fval

    def transform(self, form):
        """
        Transform validated Tally form to easier format; run validate before
        calling this method.
        """
        new_form = {}
        fields = get_nested(form, None, "data", "fields")
        # Transform Tally form
        skip_questions = []
        for i, question in self.questions.items():
            if i in skip_questions:
                continue
            field_value = self.search_field_value(self.find_fields(question, fields), question["type"])
            if field_value:
                answer = self.get_question_answer(question, field_value, fields)
                # Add processed answer to new form
                new_form[question["field"]] = answer["value"]
                # Skip questions
                skip_questions.extend(answer.get("skip", []))
        return new_form

    def get_question_answer(self, question, field_value, fields):
        """
        Get question answer from its field value.
        """
        answer = None
        if question["type"] == "MULTIPLE_CHOICE":
            for ans in question["answers"]:
                if ans["answer"] == field_value:
                    answer = self.process_answer(ans, fields)
                    break # Multiple choice allows just 1 answer
        elif question["type"] == "CHECKBOXES":
            answer = { "value": [], "skip": [] }
            for ans in question["answers"]:
                if ans["answer"] in field_value:
                    next_answer = self.process_answer(ans, fields)
                    answer["value"].append(next_answer["value"])
                    answer["skip"].extend(next_answer.get("skip", []))
            if len(answer["value"]) == 0:
                answer = None
        else:
            # Text as value
            answer = { "value": field_value }
        return answer

    def process_answer(self, answer, fields):
        """
        Process a question answer; map it to its corresponding question value (if needed).
        """
        question_value = answer.get("value", None)
        if question_value is None:
            answer["value"] = answer["answer"]
        elif isinstance(question_value, dict):
            answer["value"] = self.search_field_value(self.find_fields(question_value, fields), question_value["type"])
        return answer

    def __equal(self, this, that): # pylint: disable=no-self-use
        """
        Self-defined equal; if that is a list or dictionary, `this` should be in `that`.
        Otherwise `this` should be equal to `that`.
        """
        if isinstance(that, (dict, list)):
            return this in that
        return this == that
