# Generated by Django 4.0.1 on 2022-05-01 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crowdfunding', '0008_topdonors_pid_alter_topdonors_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topdonors',
            name='pid',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crowdfunding.public_donors', verbose_name='unregistered user id'),
        ),
        migrations.AlterField(
            model_name='topdonors',
            name='uid',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='user id'),
        ),
    ]