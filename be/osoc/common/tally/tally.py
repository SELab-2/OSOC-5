"""
Tally form (https://tally.so); method for students to register.
"""
from ..utils import getNested, assertOrRaise
import json

class TallyForm:
    """
    Validate and manipulate student register form from Tally.
    """
    def __init__(self, questions):
        self.questions = questions

    @classmethod
    def fromFile(cls, questionsFile='osoc/common/tally/questions.json'):
        """
        Create class object using a JSON file.
        """
        with open(questionsFile, 'r') as f:
            questions = json.load(f)
        return cls(questions)

    def validate(self, form):
        """
        Validate Tally form; make sure all student data is present.
        """
        assertOrRaise(form.get("eventType", None) == "FORM_RESPONSE", "Format error: Event type should be 'FORM_RESPONSE'.")
        # Get question fields from form
        fields = getNested(form, None, "data", "fields")
        assertOrRaise(fields != None, "Format error: No fields (root > data > fields).")
        # Validate (required) questions
        skipQuestions = []
        for i, question in self.questions.items():
            if not question["required"] or i in skipQuestions:
                continue
            # Required questions should have matching fields in the form
            filteredFields = self.findFields(question, fields)
            assertOrRaise(filteredFields, f"Missing question in form: {', '.join(question['question'])}.")
            # Required questions should have a value
            fieldValue = self.searchFieldValue(filteredFields, question["type"])
            assertOrRaise(fieldValue != None, f"Question is required: {', '.join(question['question'])}.")
            # Add skip values if necessary
            answer = self.getQuestionAnswer(question, fieldValue, fields)
            assertOrRaise(answer != None, f"Question has no answer: {', '.join(question['question'])}.")
            skipQuestions.extend(answer.get("skip", []))
        return form

    def findFields(self, question, fields):
        """
        Find fields that correspond with a given question.
        """
        foundFields = []
        for field in fields:
            if field["label"] in question["question"] and self.__equal(field["type"], question["type"]):
                foundFields.append(field)
        return foundFields

    def searchFieldValue(self, fields, qtype):
        """
        Search (filtered) fields for a value with a given type.
        """
        value = None
        i = 0
        while value == None and i < len(fields):
            value = self.getFieldValue(fields[i], qtype)
            i += 1
        return value

    def getFieldValue(self, field, qtype):
        """
        Get value from field with the given type.
        """
        if qtype == "MULTIPLE_CHOICE":
            optionId = field["value"]
            for option in field["options"]:
                if option["id"] == optionId:
                    return option["text"]
        elif qtype == "CHECKBOXES":
            checked = field["value"]
            values = []
            for option in field["options"]:
                if option["id"] in checked:
                    values.append(option["text"])
            return values
        else:
            # Text as value
            return field["value"]

    def transform(self, form):
        """
        Transform validated Tally form to easier format; run validate before
        calling this method.
        """
        newForm = {}
        fields = getNested(form, None, "data", "fields")
        # Transform Tally form
        skipQuestions = []
        for i, question in self.questions.items():
            if i in skipQuestions:
                continue
            fieldValue = self.searchFieldValue(self.findFields(question, fields), question["type"])
            if fieldValue:
                answer = self.getQuestionAnswer(question, fieldValue, fields)
                # Add processed answer to new form
                newForm[question["field"]] = answer["value"]
                # Skip questions
                skipQuestions.extend(answer.get("skip", []))
        return newForm

    def getQuestionAnswer(self, question, fieldValue, fields):
        """
        Get question answer from its field value.
        """
        answer = None
        if question["type"] == "MULTIPLE_CHOICE":
            for ans in question["answers"]:
                if ans["answer"] == fieldValue:
                    answer = self.processAnswer(ans, fields)
                    break # Multiple choice allows just 1 answer
        elif question["type"] == "CHECKBOXES":
            answer = { "value": [], "skip": [] }
            for ans in question["answers"]:
                if ans["answer"] in fieldValue:
                    nextAnswer = self.processAnswer(ans, fields)
                    answer["value"].append(nextAnswer["value"])
                    answer["skip"].extend(nextAnswer.get("skip", []))
            if len(answer["value"]) == 0:
                answer = None
        else:
            # Text as value
            answer = { "value": fieldValue }
        return answer

    def processAnswer(self, answer, fields):
        """
        Process a question answer; map it to its corresponding question value (if needed).
        """
        questionValue = answer.get("value", None)
        if questionValue == None:
            answer["value"] = answer["answer"]
        elif isinstance(questionValue, dict):
            answer["value"] = self.searchFieldValue(self.findFields(questionValue, fields), questionValue["type"])
        return answer

    def __equal(self, this, that):
        """
        Self-defined equal; if that is a list or dictionary, `this` should be in `that`.
        Otherwise `this` should be equal to `that`.
        """
        if isinstance(that, list) or isinstance(that, dict):
            return this in that
        else:
            return this == that
