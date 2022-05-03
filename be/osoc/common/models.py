"""
Describes the database (PostgreSQL) models.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from .utils import strip_and_lower_email


# Phone number validation
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class Skill(models.Model):
    """
    Skill; A talent or ability of a Student.
    Students can have more than one skill (many-to-many relationship).
    """
    name = models.CharField(
        _('name'),
        unique=True,
        max_length=255
    )
    color = models.CharField(
        _('color'),
        max_length=50
    )

    def __str__(self):
        return self.name


class CoachManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Coach(AbstractUser):  # models.Model):
    """
    Coach; Person who, together with other coaches, oversees
           one or more projects.
    """

    username = None

    first_name = models.CharField(
        _('name'),
        max_length=255,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=255,
    )
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    is_admin = models.BooleanField(
        _('is admin'),
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CoachManager()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        (method is required to implement by Django)
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def clean(self):
        """
        Will be called before saving.
        """
        # strip first name and last name
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()

        # strip email and transform it to lowercase
        self.email = strip_and_lower_email(self.email)

    def save(self, *args, **kwargs):
        """
        Custom save method that calls the full_clean method.
        See https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.clean_fields
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()


class GithubUser(models.Model):
    """
    Github user; used to log coaches in via github
    """
    login = models.CharField(
        _('login'),
        max_length=255,
        unique=True
    )
    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE
    )


class Student(models.Model):
    """
    Student; Person who would like to participate in an OSOC project.
    """
    class Gender(models.TextChoices):
        """
        Gender enum, gender can be Male, Female, Transgender or Unknown
        when a student chooses 'rather not tell' on the tally form (see tally.py), the Unknown state is selected here
        """
        FEMALE = '0', _('Female')
        MALE = '1', _('Male')
        TRANSGENDER = '2', _('Transgender')
        UNKNOWN = '3', _('Unknown')

    class Status(models.TextChoices):
        """
        Status should be changed when the respective email is sent
        Applied
            undecided, screening
        Awaiting project
            Coaches are looking for a project for this student, sent maybe
        Approved
            Student is approved and is able to participate, sent yes
        Contract confirmed
            Student has signed the contract
        Contract declined
            Student has declined the contract
        Rejected
            Student is rejected and is not able to participate, sent no
        """
        APPLIED = '0', _('Applied')
        AWAITING_PROJECT = '1', _('Awaiting project')
        APPROVED = '2', _('Approved')
        CONTRACT_CONFIRMED = '3', _('Contract confirmed')
        CONTRACT_DECLINED = '4', _('Contract declined')
        REJECTED = '5', _('Rejected')

    employment_agreement = models.CharField(
        _('employment agreement'),
        max_length=255,
    )
    hinder_work = models.TextField(
        _('hinder work'),
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _('name'),
        max_length=255,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=255,
    )
    call_name = models.CharField(
        _('call name'),
        max_length=255,
        blank=True,
        default=""
    )
    gender = models.CharField(
        _('gender'),
        max_length=1,
        choices=Gender.choices,
        default=Gender.UNKNOWN
    )
    pronouns = models.CharField(
        _('pronouns'),
        max_length=255,
        null=True,
        blank=True
    )
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(
        _('phone number'),
        validators=[phone_regex],
        max_length=17,
        blank=True,
        default=""
    )
    language = models.CharField(
        _('language'),
        max_length=255
    )
    english_rating = models.PositiveSmallIntegerField(
        _("english rating"),
        validators=[MaxValueValidator(5), MinValueValidator(1)],
    )
    motivation = models.TextField(
        _('motivation')
    )
    cv = models.URLField(
        _('cv'),
        max_length=255
    )
    portfolio = models.URLField(
        _('portfolio'),
        max_length=255
    )
    fun_fact = models.TextField(
        _('fun fact'),
    )
    school_name = models.CharField(
        _("school name"),
        max_length=255
    )
    degree = models.CharField(
        _("degree"),
        max_length=255
    )
    degree_duration = models.PositiveSmallIntegerField(
        _("degree duration"),
        validators=[MinValueValidator(1)],
    )
    degree_current_year = models.PositiveSmallIntegerField(
        _("degree current year"),
        validators=[MinValueValidator(1)],
    )
    studies = models.CharField(
        _("studies"),
        max_length=255
    )
    alum = models.BooleanField(
        _("alum"),
        default=False
    )
    student_coach = models.BooleanField(
        _("wants to be student coach"),
        default=False
    )
    status = models.CharField(
        _('status'),
        max_length=1,
        choices=Status.choices,
        default=Status.APPLIED
    )
    skills = models.ManyToManyField(
        Skill,
    )
    best_skill = models.CharField(
        _("best skill"),
        max_length=255
    )
    suggestions = models.ManyToManyField(
        Coach,
        through='Suggestion',
        blank=True
    )
    final_decision = models.ForeignKey(
        'Suggestion',
        on_delete=models.SET_NULL,
        related_name='final_decision_student',
        blank=True,
        null=True
    )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        (method is required to implement by Django)
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def clean(self):
        """
        Will be called before saving.
        """
        # strip first name and last name
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()

        # strip email and transform it to lowercase
        self.email = strip_and_lower_email(self.email)

    def save(self, *args, **kwargs):
        """
        Custom save method that calls the full_clean method.
        See https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.clean_fields
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()


class Project(models.Model):
    """
    Project; A project of a partner that needs skills (read: students)
             and has a number of coaches.
    """
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    partner_name = models.CharField(
        _('partner name'),
        max_length=255,
    )
    extra_info = models.TextField(
        _('extra info'),
    )
    required_skills = models.ManyToManyField(
        Skill,
        through='RequiredSkills',
    )
    coaches = models.ManyToManyField(
        Coach,
        blank=True
    )
    suggested_students = models.ManyToManyField(
        Student,
        through='ProjectSuggestion',
        blank=True
    )

    def __str__(self):
        return self.name


class RequiredSkills(models.Model):
    """
    Intermediary model; A project can need a skill N times.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        _('amount'),
        default=1,
    )
    comment = models.CharField(
        _('comment'),
        default="",
        blank=True,
        max_length=500
    )


class Suggestion(models.Model):
    """
    Suggestion; A coach can suggest whether he/she thinks a student
                can be used.
    """
    class Suggestion(models.TextChoices):
        """
        suggestion type enum, suggestion type can be Yesm No or Maybe
        when a coach selects 'undecided' for a suggestion, the suggestion is removed in the backend
        """
        YES = '0', _('Yes')
        NO = '1', _('No')
        MAYBE = '2', _('Maybe')

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    coach = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        null=True
    )
    suggestion = models.CharField(
        _('suggestion'),
        max_length=1,
        choices=Suggestion.choices,
    )
    reason = models.CharField(
        _('reason'),
        blank=True,
        default="",
        max_length=500
    )
    final = models.BooleanField(
        _('final decision'),
        default=False
    )

    class Meta:
        unique_together = (("student", "coach", "final"))

    def __str__(self):
        suggestion_label = self.Suggestion(self.suggestion).label
        return f"{suggestion_label}: {self.reason}"


class ProjectSuggestion(models.Model):
    """
    Intermediary model; A coach can suggest a student for a project.
    """
    reason = models.CharField(
        _('reason'),
        blank=True,
        default="",
        max_length=500
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True
    )
    coach = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        null=True
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.RESTRICT   # not allowed to delete a skill that is used in a suggestion
    )


class SentEmail(models.Model):
    """
    Information about which emails have been sent to which students
    """
    sender = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        null=True
    )
    receiver = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True
    )
    time = models.DateTimeField(
        _("send date and time"),
        default=timezone.now,
        blank=True
    )
    info = models.CharField(
        _("email info"),
        max_length=255,
        blank=True,
        default=""
    )

    def __str__(self):
        return f"{self.info} (from: {self.sender}, to: {self.receiver})"
