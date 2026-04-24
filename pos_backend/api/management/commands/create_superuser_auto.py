"""
Automatic superuser creation for Render deployment (no shell access).
Reads credentials from environment variables. Safe to run on every deploy —
skips creation if the user already exists.

Environment Variables Required:
    DJANGO_SUPERUSER_USERNAME  (e.g. admin)
    DJANGO_SUPERUSER_EMAIL     (e.g. admin@example.com)
    DJANGO_SUPERUSER_PASSWORD  (e.g. YourStrongPassword123)

Usage:
    python manage.py create_superuser_auto
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import AuthAdmin


class Command(BaseCommand):
    help = 'Auto-create superuser + AuthAdmin from environment variables (safe for repeated deploys)'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        # ── Validate env vars ──
        if not all([username, email, password]):
            self.stdout.write(self.style.WARNING(
                '⚠️  Skipping auto superuser creation — '
                'DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, '
                'and DJANGO_SUPERUSER_PASSWORD must all be set.'
            ))
            return

        # ── Django superuser ──
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f'✅ Django superuser "{username}" already exists — skipping.'
            ))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(
                f'✅ Django superuser "{username}" created successfully.'
            ))

        # ── AuthAdmin table entry ──
        if AuthAdmin.objects.filter(email=email).exists():
            self.stdout.write(self.style.SUCCESS(
                f'✅ AuthAdmin entry for "{email}" already exists — skipping.'
            ))
        else:
            admin = AuthAdmin(
                name=username,
                email=email,
            )
            admin.set_password(password)
            admin.save()
            self.stdout.write(self.style.SUCCESS(
                f'✅ AuthAdmin entry for "{email}" created successfully.'
            ))

        self.stdout.write(self.style.SUCCESS('🎉 Auto superuser setup complete!'))
