"""
Admin seeding removed.
Create admin accounts using Django's built-in superuser system:

    python manage.py createsuperuser

Only users with is_staff=True or is_superuser=True can log in to the POS dashboard.
"""


def seed_admin():
    """No-op – admin accounts are managed via `createsuperuser`."""
    pass
