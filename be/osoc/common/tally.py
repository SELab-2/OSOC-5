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

        for i, question in self.questions.items():
            print(question)

    def validate(self, form):
        """
        Validate Tally form; make sure all student data is present.
        """
        if form.get("eventType", None) != "FORM_RESPONSE":
            raise self.TallyFormError("Not a Tally form")
        fields = getNested(form, None, "data", "fields")
        if fields == None:
            raise self.TallyFormError("Not a Tally form")
        # Questions should be in the fields as formatted
        for question in self.questions:
            pass

    def transform(self, form):
        """
        Transform validate Tally form to python dictionary with accessible fields.
        """
        pass
