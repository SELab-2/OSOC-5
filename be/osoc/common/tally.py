"""
Tally form (https://tally.so); method for students to register.
"""
from .utils import getNested, assertOrRaise
import json

class TallyForm:
    """
    Validate and manipulate student register form from Tally.
    """
    def __init__(self, questions):
        self.questions = questions

    @classmethod
    def fromFile(cls, questionsFile='osoc/common/tally/questions.json'):
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
            assertOrRaise(filteredFields, f"Missing question in form {';'.join(question['question'])}")
            # Required questions should have a value
            fieldValue = self.searchFieldValue(filteredFields, question["type"])
            assertOrRaise(fieldValue != None, f"Question is required {';'.join(question['question'])}")
            # Add skip values if necessary
            if fieldValue:
                skipQuestions.extend(self.getAnswer(fieldValue, question.get("answers", [])).get("skip", []))
        return form

    def findFields(self, question, fields):
        """
        Find fields that correspond with a given question.
        """
        foundFields = []
        for field in fields:
            if field["label"] in question["question"] and self.__hasEqualType(question["type"], field["type"]):
                foundFields.append(field)
        return foundFields

    def __hasEqualType(self, questionType, fieldType):
        """
        Verify equal question and field type.
        """
        if isinstance(questionType, list):
            return fieldType in questionType
        else:
            return fieldType == questionType

    def searchFieldValue(self, fields, type):
        """
        Search (filtered) fields for a value with a given type.
        """
        value = None
        i = 0
        while value == None and i < len(fields):
            value = self.getFieldValue(fields[i], type)
            i += 1
        return value

    def getFieldValue(self, field, type):
        """
        Get value from field with the given type.
        """
        if type == "MULTIPLE_CHOICE":
            optionId = field["value"]
            for option in field["options"]:
                if option["id"] == optionId:
                    return option["text"]
        elif type == "CHECKBOXES":
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
                answer = self.getAnswer(fieldValue, question.get("answers", []))
                # Add processed answer to new form
                newForm[question["field"]] = self.processAnswer(answer, fields)
                # Skip questions
                skipQuestions.extend(answer.get("skip", []))
        return newForm

    def getAnswer(self, fieldValue, answers):
        """
        Get question answer from its field value.
        """
        # TODO: fieldValue can be a list with CHECKBOXES; handle checkboxes
        answerBody = None
        for answer in answers:
            if answer["answer"] == fieldValue:
                answerBody = answer
        return { 'answer': fieldValue } if answerBody == None else answerBody

    def processAnswer(self, answer, fields):
        """
        Process a question answer; map it to its corresponding qeustion value.
        """
        # TODO: adjust accordingly when getAnswer changes
        questionValue = answer.get("value", None)
        if questionValue == None:
            return answer["answer"]
        else:
            # Question value is another question
            if isinstance(questionValue, dict):
                return self.searchFieldValue(self.findFields(questionValue, fields), questionValue["type"])
            # Question value is just a value
            else:
                return questionValue
