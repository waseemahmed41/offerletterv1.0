# Generated manually to fix Template model db_table issue

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_alter_offerletter_options_alter_template_options_and_more'),
    ]

    operations = [
        # No database operations needed - table already exists as 'templates'
        # This migration just records the model Meta.db_table change
    ]
