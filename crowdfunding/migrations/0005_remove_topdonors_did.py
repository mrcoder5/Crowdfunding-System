# Generated by Django 4.0.1 on 2022-04-30 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0004_public_donors_transactions_pid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topdonors',
            name='did',
        ),
    ]
