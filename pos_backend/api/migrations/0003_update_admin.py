from django.db import migrations


def update_admin(apps, schema_editor):
    """Update or create admin with new credentials."""
    Admin = apps.get_model('api', 'Admin')
    # Remove any old admin records
    Admin.objects.all().delete()
    # Insert new admin
    Admin.objects.create(
        username='contact@vstechmfg.com',
        password='Subvig@261095'
    )


def reverse_admin(apps, schema_editor):
    Admin = apps.get_model('api', 'Admin')
    Admin.objects.filter(username='contact@vstechmfg.com').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_seed_admin'),
    ]

    operations = [
        migrations.RunPython(update_admin, reverse_admin),
    ]
