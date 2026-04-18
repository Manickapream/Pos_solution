"""
Custom management command to create a POS admin.
Creates both a Django superuser AND saves credentials in the auth_admin table.

Usage:
    python manage.py createadmin
"""
import getpass
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import AuthAdmin


class Command(BaseCommand):
    help = 'Create a POS admin (Django superuser + auth_admin table entry)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n═══ POS Admin Creator ═══\n'))

        # 1. Collect admin details
        name = input('Full Name: ').strip()
        if not name:
            self.stdout.write(self.style.ERROR('Error: Name cannot be blank.'))
            return

        email = input('Email: ').strip()
        if not email:
            self.stdout.write(self.style.ERROR('Error: Email cannot be blank.'))
            return

        username = input('Username: ').strip()
        if not username:
            self.stdout.write(self.style.ERROR('Error: Username cannot be blank.'))
            return

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'Error: Username "{username}" already exists.'))
            return

        # Check if email already exists in auth_admin
        if AuthAdmin.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'Error: Email "{email}" already exists in auth_admin.'))
            return

        # 2. Password with confirmation
        while True:
            password = getpass.getpass('Password: ')
            if not password:
                self.stdout.write(self.style.ERROR('Error: Password cannot be blank.'))
                continue

            confirm_password = getpass.getpass('Confirm Password: ')
            if password != confirm_password:
                self.stdout.write(self.style.ERROR('Error: Passwords do not match. Try again.\n'))
                continue

            if len(password) < 8:
                self.stdout.write(self.style.WARNING(
                    'Warning: Password is less than 8 characters.'
                ))
                proceed = input('Continue anyway? (y/N): ').strip().lower()
                if proceed != 'y':
                    continue

            break

        # 3. Create Django superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=name.split()[0] if name else '',
                last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
            )
            self.stdout.write(self.style.SUCCESS(
                f'✓ Django superuser "{username}" created successfully.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
            return

        # 4. Save to auth_admin table
        try:
            admin = AuthAdmin(
                name=name,
                email=email,
            )
            admin.set_password(password)  # Hash the password
            admin.save()
            self.stdout.write(self.style.SUCCESS(
                f'✓ Auth admin record saved to "auth_admin" table.'
            ))
        except Exception as e:
            # Rollback superuser if auth_admin save fails
            user.delete()
            self.stdout.write(self.style.ERROR(f'Error saving to auth_admin: {e}'))
            return

        # 5. Summary
        self.stdout.write(self.style.MIGRATE_HEADING('\n═══ Admin Created Successfully ═══'))
        self.stdout.write(f'  Name     : {name}')
        self.stdout.write(f'  Email    : {email}')
        self.stdout.write(f'  Username : {username}')
        self.stdout.write(f'  Role     : Superuser / Admin')
        self.stdout.write(self.style.MIGRATE_HEADING('═══════════════════════════════════\n'))
