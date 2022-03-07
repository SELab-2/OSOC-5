import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .utils import strip_and_lower_email

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class Skill(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
        primary_key=True
    )
    description = models.CharField(
        _('description'),
        max_length=255
    )


class Student(models.Model):
    class Language(models.TextChoices):
        DUTCH = '0', _('Dutch')
        ENGLISH = '1', _('English')
        FRENCH = '2', _('French')
        GERMAN = '3', _('German')
        OTHER = '4', _('Other')

    first_name = models.CharField(
        _('name'),
        max_length=255,
    )
    surname = models.CharField(
        _('surname'),
        max_length=255,
    )
    call_name = models.CharField(
        _('call name'),
        max_length=255,
        default="",
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
        null=True
    )
    language = models.CharField(
        _('language'),
        max_length=1,
        choices=Language.choices,
        default=Language.DUTCH,
    )
    extra_info = models.TextField(
        _('extra info'),
        blank=True,
        null=True
    )
    cv = models.URLField(
        _('cv'),
        max_length=200
    )
    portfolio = models.URLField(
        _('portfolio'),
        max_length=200
    )
    last_email_sent = models.DateTimeField(
        _('last email sent'),
        null=True
    )
    school_name = models.CharField(
        _("school name"),
        max_length=255
    )
    degree = models.CharField(
        _("degree"),
        max_length=255
    )
    studies = models.CharField(
        _("studies"),
        max_length=255
    )
    """
    other fields necessary?
    from tally form: total degree years, current degree year, 
    best skill, previously participated in osoc, willing to be student coach
    """


    skills = models.ManyToManyField(
        Skill,
        on_delete=models.CASCADE
    )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        (method is required to implement by Django)
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
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
        See https://docs.djangoproject.com/en/dev/ref/models/instances/
        #django.db.models.Model.clean_fields
        """
        self.full_clean()
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()


class Coach(models.Model):

    first_name = models.CharField(
        _('name'),
        max_length=255,
    )
    surname = models.CharField(
        _('surname'),
        max_length=255,
    )
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    isAdmin = models.BooleanField(
        _('is admin'),
        default=False
    )
    last_email_sent = models.DateTimeField(
        _('last email sent')
    )
    suggestions = models.ManyToManyField(
        Student,
        through='Suggestion',
        on_delete=models.CASCADE,
    )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        (method is required to implement by Django)
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
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
        See https://docs.djangoproject.com/en/dev/ref/models/instances/
        #django.db.models.Model.clean_fields
        """
        self.full_clean()
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()


class Project(models.Model):

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
    skills = models.ManyToManyField(
        Skill,
        through='Project_needs_skills',
        on_delete=models.CASCADE,
    )
    coaches = models.ManyToManyField(
        Coach,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Project_needs_skills(models.Model):
    """
    intermediary model
    this is needed because an amount of this skill needed must be specified
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


class Suggestion(models.Model):
    class Suggestion(models.TextChoices):
        YES = '0', _('Yes')
        NO = '1', _('No')
        MAYBE = '2', _('Maybe')

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE
    )

    suggestion = models.CharField(
        _('suggestion'),
        max_length=1,
        choices=Suggestion.choices,
        default=None,
    )
    reason = models.TextField(
        _('reason'),
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.suggestion}: {self.reason}"


class Project_suggestion(models.Model):
    """
    intermediary model
    a coach can suggest a student for a project
    -> three way relation
    """

    reason = models.TextField(
        _('reason'),
        blank=True,
        null=True
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )
    
    class Meta:
        unique_together = (("project", "student", "coach"),)