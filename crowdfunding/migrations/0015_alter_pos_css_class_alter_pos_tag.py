# Generated by Django 4.0.1 on 2022-05-05 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0014_pos_css_class_alter_transactions_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pos',
            name='css_class',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pos',
            name='tag',
            field=models.TextField(default=''),
        ),
    ]