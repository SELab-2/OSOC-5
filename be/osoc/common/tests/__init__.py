from factory.django import DjangoModelFactory
from factory import SubFactory
from osoc.common.models import Project, SentEmail, Skill, Student, Coach


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student
    first_name="Jonathan"
    last_name="Doe"
    call_name="John"
    email="student@example.com"
    phone_number="+14255550123"
    language="dutch"
    cv="https://example.com"
    portfolio="https://example.com"
    school_name="example"
    degree="example"
    studies="example"
    alum=False
    employment_agreement="example"
    english_rating=2
    motivation="example"
    fun_fact="example"
    degree_duration=2
    degree_current_year=1
    best_skill="example"


class SkillFactory(DjangoModelFactory):
    class Meta:
        model = Skill
    name="skill"
    color="blue"


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project
    name="project"
    partner_name="partner"
    extra_info="extra info"


class CoachFactory(DjangoModelFactory):
    class Meta:
        model = Coach
    first_name="Jane"
    last_name="Doe"
    email="coach@example.com"
    password="Pas$w0rd"


class AdminFactory(CoachFactory):
    class Meta:
        model = Coach
    is_admin=True


class SentEmailFactory(DjangoModelFactory):
    class Meta:
        model = SentEmail
    sender=SubFactory(CoachFactory)
    receiver=SubFactory(StudentFactory)
    info="email info"
