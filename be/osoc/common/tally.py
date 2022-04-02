"""
Tally form (https://tally.so); method for students to register.
"""
from .utils import getNested
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

    def __init__(self, questions):
        self.questions = questions

    @classmethod
    def fromFile(cls, questionsFile='osoc/common/tally/questions.json'):
        with open(questionsFile, 'r') as f:
            questions = json.load(f)
        return cls(questions)

    @classmethod
    def fromDict(cls, questions):
        return cls(questions)

    def validate(self, form):
        """
        Validate Tally form; make sure all student data is present.
        """
        fields = getNested(form, None, "data", "fields")
        self.__raiseIfTrue(form.get("eventType", None) != "FORM_RESPONSE", "Format error", "Event type should be 'FORM_RESPONSE'")
        self.__raiseIfTrue(fields == None, "Format error", "No fields (root > data > fields)!")
        # Questions should be in the fields as formatted
        for i, question in self.questions.items():
            # just check required questions
            if not self.__gor(question, "required"):
                continue
            matching = self.findFields(question, fields)
            # required questions should have matching fields in the form
            self.__raiseIfTrue(not matching, "Missing question in form", ";".join(self.__gor(question, "question")))

            value = None
            i = 0
            while value == None and i < len(matching):
                # TODO: add skip values
                value = self.getFieldValue(matching[i], question["type"])
                i += 1
            # required questions should have a value
            self.__raiseIfTrue(value == None, "Question is required", ";".join(self.__gor(question, "question")))
        return form

    def __raiseIfTrue(self, check, mesg, extra):
        """
        Raise Tally error if check if true; with message and extra detailed info.
        """
        if check: # if check passed, raise error
            raise self.TallyFormError(f'{mesg}: {extra}')

    def __gor(self, d, k):
        """
        Get or raise field error; basically KeyError wrapped inside a TallyFormError.
        """
        try:
            return d[k]
        except KeyError:
            raise self.TallyFormError(f'Field not present: {k}')

    def findFields(self, question, fields):
        """
        Find fields (from a Tally form) that correspond with the given question.
        """
        matching = []
        for field in fields:
            if self.__gor(field, "label") in self.__gor(question, "question") and self.__hasEqualType(self.__gor(question, "type"), self.__gor(field, "type")):
                matching.append(field)
        return matching

    def __hasEqualType(self, questionType, fieldType):
        """
        Verify equal question and field type.
        """
        if isinstance(questionType, list):
            return fieldType in questionType
        else:
            return fieldType == questionType

    def getFieldValue(self, field, fieldType):
        """
        Get value from field with the given type.
        """
        if fieldType == "MULTIPLE_CHOICE":
            optionId = self.__gor(field, "value")
            for option in self.__gor(field, "options"):
                if self.__gor(option, "id") == optionId:
                    return self.__gor(option, "text")
        elif fieldType == "CHECKBOXES":
            checked = self.__gor(field, "value")
            values = []
            for option in self.__gor(field, "options"):
                if self.__gor(option, "id") in checked:
                    values.append(self.__gor(option, "text"))
            return values
        else:
            # assume text as value
            return self.__gor(field, "value")

    def transform(self, form):
        """
        Transform validate Tally form to python dictionary with accessible fields;
        this function does not validate fields, make sure to run validate before
        running this function.
        """
        newForm = {}
        fields = getNested(form, None, "data", "fields")
        for i, question in self.questions.items():
            # only required questions need to be checked when validating
            twinFields = self.findQuestions(question, fields)

            value = None
            for field in twinFields:
                value = self.getFieldValue(field, question["type"])
                if value:
                    break
            if value:
                # TODO: map based on value type and set rules for if question already in newForm
                newForm[question["field"]] = self.mapValue(value, question.get("answers", None))
        return newForm

    def mapValue(self, value, answers):
        if answers == None:
            return value

        for answer in answers:
            if answer["answer"] == value:
                return answer.get("value", value)
