# Generated by Django 3.2.13 on 2022-05-10 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentemail',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'Confirmation'), ('1', 'Rejection'), ('2', 'Hold on tight'), ('3', 'Contract'), ('4', 'Other')], max_length=1, null=True, verbose_name='type'),
        ),
    ]
