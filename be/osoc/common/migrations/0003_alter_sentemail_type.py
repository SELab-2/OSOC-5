# Generated by Django 3.2.13 on 2022-05-10 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_sentemail_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentemail',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'Applied'), ('1', 'Awaiting project'), ('2', 'Approved'), ('3', 'Contract confirmed'), ('4', 'Contract declined'), ('5', 'Rejected')], max_length=1, null=True, verbose_name='type'),
        ),
    ]