# Generated by Django 4.0.3 on 2022-03-04 16:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='name')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('level', models.SmallIntegerField(verbose_name='level')),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('suggestion', models.CharField(choices=[('0', 'Yes'), ('1', 'No'), ('2', 'Maybe')], default=None, max_length=1, verbose_name='suggestion')),
                ('reason', models.TextField(verbose_name='reason')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('first_name', models.CharField(max_length=255, verbose_name='name')),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('call_name', models.CharField(default='', max_length=255, verbose_name='call name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number')),
                ('language', models.CharField(choices=[('0', 'Dutch'), ('1', 'English'), ('2', 'French'), ('3', 'German'), ('4', 'Other')], default='0', max_length=1, unique=True, verbose_name='language')),
                ('extra_info', models.TextField(verbose_name='extra info')),
                ('cv', models.URLField(verbose_name='cv')),
                ('portfolio', models.URLField(verbose_name='portfolio')),
                ('last_email_sent', models.DateTimeField(verbose_name='last email sent')),
                ('skills', models.ManyToManyField(to='osoc.skill')),
                ('suggestions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='osoc.suggestion')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('partner_name', models.CharField(max_length=255, verbose_name='partner name')),
                ('extra_info', models.TextField(verbose_name='extra info')),
                ('skills', models.ManyToManyField(to='osoc.skill')),
                ('students', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='osoc.student')),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('first_name', models.CharField(max_length=255, verbose_name='name')),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('isAdmin', models.BooleanField(default=False, verbose_name='is admin')),
                ('last_email_sent', models.DateTimeField(verbose_name='last email sent')),
                ('has_projects', models.ManyToManyField(to='osoc.project')),
                ('suggestions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='osoc.suggestion')),
            ],
        ),
    ]
