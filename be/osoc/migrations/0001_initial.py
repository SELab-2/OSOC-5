# Generated by Django 4.0.3 on 2022-03-08 15:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('isAdmin', models.BooleanField(default=False, verbose_name='is admin')),
                ('last_email_sent', models.DateTimeField(verbose_name='last email sent')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('partner_name', models.CharField(max_length=255, verbose_name='partner name')),
                ('extra_info', models.TextField(verbose_name='extra info')),
                ('coaches', models.ManyToManyField(to='osoc.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='name')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('call_name', models.CharField(default='', max_length=255, verbose_name='call name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number')),
                ('language', models.CharField(choices=[('0', 'Dutch'), ('1', 'English'), ('2', 'French'), ('3', 'German'), ('4', 'Other')], default='0', max_length=1, verbose_name='language')),
                ('extra_info', models.TextField(blank=True, null=True, verbose_name='extra info')),
                ('cv', models.URLField(verbose_name='cv')),
                ('portfolio', models.URLField(verbose_name='portfolio')),
                ('last_email_sent', models.DateTimeField(null=True, verbose_name='last email sent')),
                ('school_name', models.CharField(max_length=255, verbose_name='school name')),
                ('degree', models.CharField(max_length=255, verbose_name='degree')),
                ('studies', models.CharField(max_length=255, verbose_name='studies')),
                ('skills', models.ManyToManyField(to='osoc.skill')),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion', models.CharField(choices=[('0', 'Yes'), ('1', 'No'), ('2', 'Maybe')], default=None, max_length=1, verbose_name='suggestion')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='reason')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.coach')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.student')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectNeedsSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1, verbose_name='amount')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.project')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.skill')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(through='osoc.ProjectNeedsSkills', to='osoc.skill'),
        ),
        migrations.AddField(
            model_name='coach',
            name='suggestions',
            field=models.ManyToManyField(through='osoc.Suggestion', to='osoc.student'),
        ),
        migrations.CreateModel(
            name='ProjectSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='reason')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.coach')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.project')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.skill')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osoc.student')),
            ],
            options={
                'unique_together': {('project', 'student', 'coach')},
            },
        ),
    ]
