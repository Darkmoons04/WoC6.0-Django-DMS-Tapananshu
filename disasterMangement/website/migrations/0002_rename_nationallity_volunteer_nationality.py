# Generated by Django 5.0 on 2024-01-20 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='volunteer',
            old_name='nationallity',
            new_name='nationality',
        ),
    ]
