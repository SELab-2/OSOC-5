"""
Tally form (https://tally.so); method for students to register.
"""
import json

class TallyForm:
    """
    Validate and manipulate student register form from Tally.
    """
    def __init__(self, questionsFile='osoc/common/tally/questions.json'):
        with open(questionsFile, 'r') as f:
            self.questions = json.load(f)

    def validate(self, form):
        """
        Validate Tally form; make sure all student data is present.
        """
        pass

    def transform(self, form):
        """
        Transform validate Tally form to python dictionary with accessible fields.
        """
        pass
