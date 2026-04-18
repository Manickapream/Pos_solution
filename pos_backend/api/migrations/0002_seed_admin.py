from django.db import migrations


def seed_admin(apps, schema_editor):
    """Insert default admin user if none exists."""
    Admin = apps.get_model('api', 'Admin')
    if not Admin.objects.exists():
        Admin.objects.create(
            username='contact@vstechmfg.com',
            password='Subvig@261095'
        )


def remove_admin(apps, schema_editor):
    """Reverse: remove the seeded admin."""
    Admin = apps.get_model('api', 'Admin')
    Admin.objects.filter(username='Admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_admin, remove_admin),
    ]
