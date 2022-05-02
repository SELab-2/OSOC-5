"""
test module init file
defines some factory classes to use in tests
"""
from factory.django import DjangoModelFactory
from factory import SubFactory
from osoc.common.models import Project, SentEmail, Skill, Student, Coach


class StudentFactory(DjangoModelFactory):
    """
    student factory
    create student by calling StudentFactory()
    if you want to create multiple students,
    call StudentFactory(email="...") with different emails
    """
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
    """
    skill factory
    create skill by calling SkillFactory()
    if you want to create multiple skills,
    call SkillFactory(name="...") with different names
    """
    class Meta:
        model = Skill
    name="skill"
    color="blue"


class ProjectFactory(DjangoModelFactory):
    """
    project factory
    create project by calling ProjectFactory()
    if you want to create multiple projects,
    call ProjectFactory(name="...") with different names
    """
    class Meta:
        model = Project
    name="project"
    partner_name="partner"
    extra_info="extra info"


class CoachFactory(DjangoModelFactory):
    """
    coach factory
    create coach by calling CoachFactory()
    if you want to create multiple coaches,
    call CoachFactory(email="...") with different emails
    """
    class Meta:
        model = Coach
    first_name="Jane"
    last_name="Doe"
    email="coach@example.com"
    password="Pas$w0rd"


class AdminFactory(CoachFactory):
    """
    admin factory
    create admin by calling AdminFactory()
    same as CoachFactory, but is_admin is true
    """
    class Meta:
        model = Coach
    is_admin=True


class SentEmailFactory(DjangoModelFactory):
    """
    sentemail factory
    create sentemail by calling SentEmailFactory()
    call SentEmailFactory(sender=coach, receiver=student)
    if you want to create a sentemail object with existing sender/receiver
    call SentEmailFactory(time=timezone object) if you want to set time
    """
    class Meta:
        model = SentEmail
    sender=SubFactory(CoachFactory)
    receiver=SubFactory(StudentFactory)
    info="email info"
