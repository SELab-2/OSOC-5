"""
Tally form (https://tally.so); method for students to register.
"""
from utils import getNested
import json

class TallyForm:
    """
    Validate and manipulate student register form from Tally.
    """
    class TallyFormError(Exception):
        """
        Raised when there is an error validating the Tally form.
        """
        pass

    def __init__(self, questionsFile='osoc/common/tally/questions.json'):
        with open(questionsFile, 'r') as f:
            self.questions = json.load(f)

    def validate(self, form):
        """
        Validate Tally form; make sure all student data is present.
        """
        fields = getNested(form, None, "data", "fields")
        if form.get("eventType", None) != "FORM_RESPONSE" or fields == None:
            raise self.TallyFormError("Format error")
        # Questions should be in the fields as formatted
        # TODO: add skip values
        for i, question in self.questions.items():
            if not question["required"]:
                continue
            twinFields = self.findQuestions(question, fields)

            value = None
            for field in twinFields:
                value = self.getFieldValue(field, question["type"])
                if value:
                    break
            if value == None:
                raise self.TallyFormError("Question is required")
        return form

    def findQuestions(self, question, fields):
        """
        Find a question (self.questions) in the fields of a Tally form.
        """
        twinFields = []
        for field in fields:
            if field["label"] in question["question"]:
                twinFields.append(field)

        if question["required"] and not twinFields: # still empty
            raise self.TallyFormError("Unable to find question in Tally form")
        return twinFields

    def getFieldValue(self, field, fieldType):
        """
        Get value from field with the given type.
        """
        if fieldType == "TEXT":
            return field["value"]
        elif fieldType == "MULTIPLE_CHOICE":
            optionId = field["value"]
            for option in field["options"]:
                if option["id"] == optionId:
                    return option["text"]
        elif fieldType == "CHECKBOXES":
            checked = field["value"]
            values = []
            for option in field["options"]:
                if option["id"] in checked:
                    values.append(option["text"])
            return values
        else:
            raise self.TallyFormError("Unknown question type")

    def transform(self, form):
        """
        Transform validate Tally form to python dictionary with accessible fields.
        """
        pass
