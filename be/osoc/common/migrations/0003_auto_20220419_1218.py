# Generated by Django 3.2.12 on 2022-04-19 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('0', 'Applied'), ('1', 'Awaiting project'), ('2', 'Approved'), ('3', 'Contract confirmed'), ('4', 'Contract declined'), ('5', 'Rejected')], default='0', max_length=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='projectsuggestion',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='common.skill'),
        ),
        migrations.AlterUniqueTogether(
            name='projectsuggestion',
            unique_together=set(),
        ),
    ]