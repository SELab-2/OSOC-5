# Generated by Django 4.0.3 on 2022-03-28 12:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=255, verbose_name='name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_admin', models.BooleanField(default=False, verbose_name='is admin')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('last_email_sent', models.DateTimeField(blank=True, null=True, verbose_name='last email sent')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('partner_name', models.CharField(max_length=255, verbose_name='partner name')),
                ('extra_info', models.TextField(verbose_name='extra info')),
                ('coaches', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('color', models.CharField(max_length=50, verbose_name='color')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('call_name', models.CharField(blank=True, default='', max_length=255, verbose_name='call name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, default='', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number')),
                ('language', models.CharField(choices=[('0', 'Dutch'), ('1', 'English'), ('2', 'French'), ('3', 'German'), ('4', 'Other')], default='0', max_length=1, verbose_name='language')),
                ('extra_info', models.TextField(blank=True, default='', verbose_name='extra info')),
                ('cv', models.URLField(verbose_name='cv')),
                ('portfolio', models.URLField(verbose_name='portfolio')),
                ('last_email_sent', models.DateTimeField(blank=True, null=True, verbose_name='last email sent')),
                ('school_name', models.CharField(max_length=255, verbose_name='school name')),
                ('degree', models.CharField(max_length=255, verbose_name='degree')),
                ('studies', models.CharField(max_length=255, verbose_name='studies')),
                ('alum', models.BooleanField(default=False, verbose_name='alum')),
                ('skills', models.ManyToManyField(to='common.skill')),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion', models.CharField(choices=[('0', 'Yes'), ('1', 'No'), ('2', 'Maybe')], max_length=1, verbose_name='suggestion')),
                ('reason', models.CharField(blank=True, default='', max_length=500, verbose_name='reason')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.student')),
            ],
            options={
                'unique_together': {('student', 'coach')},
            },
        ),
        migrations.AddField(
            model_name='student',
            name='suggestions',
            field=models.ManyToManyField(blank=True, through='common.Suggestion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RequiredSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1, verbose_name='amount')),
                ('comment', models.CharField(blank=True, default='', max_length=500, verbose_name='comment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.project')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.skill')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, default='', max_length=500, verbose_name='reason')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.project')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.skill')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.student')),
            ],
            options={
                'unique_together': {('project', 'student', 'coach')},
            },
        ),
        migrations.AddField(
            model_name='project',
            name='required_skills',
            field=models.ManyToManyField(through='common.RequiredSkills', to='common.skill'),
        ),
        migrations.AddField(
            model_name='project',
            name='suggested_students',
            field=models.ManyToManyField(blank=True, through='common.ProjectSuggestion', to='common.student'),
        ),
    ]
