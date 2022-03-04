from asyncio.windows_events import NULL
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
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
    level = models.SmallIntegerField(
        _('level')
    )


class Suggestion(models.Model):
    class Suggestion(models.TextChoices):
        YES = '0', _('Yes')
        NO = '1', _('No')
        MAYBE = '2', _('Maybe')

    id = models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4,
    )
    suggestion = models.CharField(
        _('suggestion'),
        max_length=1,
        choices=Suggestion.choices,
        default=NULL,
    )
    reason = models.TextField(
        _('reason')
    )

    def __str__(self):
        return f"{self.suggestion}: {self.reason}"


class Student(models.Model):
    class Language(models.TextChoices):
        DUTCH = '0', _('Dutch')
        ENGLISH = '1', _('English')
        FRENCH = '2', _('French')
        GERMAN = '3', _('German')
        OTHER = '4', _('Other')

    id = models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4,
    )
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
        blank=True
    )
    language = models.CharField(
        _('language'),
        max_length=1,
        choices=Language.choices,
        default=Language.DUTCH,
        unique=True
    )
    extra_info = models.TextField(
        _('extra info'),
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
        _('last email sent')
    )
    skills = models.ManyToManyField(
        Skill,
        related_name="name",
    )
    suggestions = models.ForeignKey(
        Suggestion,
        related_name='suggestion',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
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
    id = models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4,
    )
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
        related_name="name"
    )
    students = models.ForeignKey(
        Student,
        related_name=Student.get_full_name(),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Coach(models.Model):
    id = models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4,
    )
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
    has_projects = models.ManyToManyField(
        Project,
        related_name="name"
    )
    suggestions = models.ForeignKey(
        Suggestion,
        related_name="suggestion",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
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
