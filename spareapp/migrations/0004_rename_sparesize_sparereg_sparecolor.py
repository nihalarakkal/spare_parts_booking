# Generated by Django 5.1.5 on 2025-01-24 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0003_rename_sparerpic_sparereg_sparepic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sparereg',
            old_name='sparesize',
            new_name='sparecolor',
        ),
    ]
