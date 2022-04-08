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

    def validate(self, form):
        """
        Validate Tally form; make sure all student data is present.
        """
        fields = getNested(form, None, "data", "fields")
        self.__raiseIfTrue(form.get("eventType", None) != "FORM_RESPONSE", "Format error", "Event type should be 'FORM_RESPONSE'")
        self.__raiseIfTrue(fields == None, "Format error", "No fields (root > data > fields)!")
        # Questions should be in the fields as formatted
        skip = []
        for i, question in self.questions.items():
            # just check required questions
            if not self.__gor(question, "required") or i in skip:
                continue
            matching = self.findFields(question, fields)
            # required questions should have matching fields in the form
            self.__raiseIfTrue(not matching, "Missing question in form", ";".join(self.__gor(question, "question")))

            value = None
            i = 0
            while value == None and i < len(matching):
                value = self.getFieldValue(matching[i], question["type"])
                skip.extend(self.__getAnswer(value, question.get("answers", [])).get("skip", []))
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
        transformed = {}
        fields = getNested(form, None, "data", "fields")
        for i, question in self.questions.items():
            # only required questions need to be checked when validating
            matching = self.findFields(question, fields)

            value = None
            i = 0
            while value == None and i < len(matching):
                value = self.getFieldValue(matching[i], question["type"])
                i += 1

            if value:
                answer = self.__getAnswer(value, question.get("answers", []))
                transformed[question["field"]] = self.__processAnswer(answer, fields)

        return transformed

    def __getAnswer(self, value, answers):
        answerBody = None
        for answer in answers:
            if self.__gor(answer, "answer") == value:
                answerBody = answer
        return { 'answer': value } if answerBody == None else answerBody

    def __processAnswer(self, answer, fields):
        value = answer.get("value", None)
        if value == None:
            return answer["answer"]
        else:
            if value.get("question", None) != None:
                matching = self.findFields(value, fields)
                newValue = None
                i = 0
                while newValue == None and i < len(matching):
                    newValue = self.getFieldValue(matching[i], value["type"])
                    i += 1
                assert value != None
                return value
            else:
                return value
