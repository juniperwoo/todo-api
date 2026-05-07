from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='CREATE SCHEMA IF NOT EXISTS pitech;',
        ),
    ]