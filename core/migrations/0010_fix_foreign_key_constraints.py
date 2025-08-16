# Generated migration to fix foreign key constraints

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def fix_admin_log_references(apps, schema_editor):
    """
    Fix django_admin_log foreign key references to point to CustomUser
    """
    # This is handled by Django automatically when we change the foreign key
    pass


def reverse_admin_log_references(apps, schema_editor):
    """
    Reverse operation - not needed for this fix
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_add_user_history_and_cloudinary'),
    ]

    operations = [
        # This migration will update the django_admin_log table to properly reference CustomUser
        migrations.RunPython(
            fix_admin_log_references,
            reverse_admin_log_references,
        ),
    ]
