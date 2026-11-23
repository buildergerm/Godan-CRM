from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create an initial Django superuser from temporary environment variables."

    def handle(self, *args, **options):
        import os

        email = os.environ.get("GODAN_BOOTSTRAP_ADMIN_EMAIL", "").strip().lower()
        password = os.environ.get("GODAN_BOOTSTRAP_ADMIN_PASSWORD", "")
        name = os.environ.get("GODAN_BOOTSTRAP_ADMIN_NAME", "").strip()

        if not email or not password:
            raise CommandError(
                "GODAN_BOOTSTRAP_ADMIN_EMAIL and "
                "GODAN_BOOTSTRAP_ADMIN_PASSWORD must both be set."
            )
        if len(password) < 16:
            raise CommandError("Bootstrap admin password must be at least 16 characters.")

        User = get_user_model()
        user = User.objects.filter(email__iexact=email).first()
        if user:
            if user.is_staff and user.is_superuser:
                self.stdout.write("Bootstrap admin already exists; no changes made.")
                return
            raise CommandError(
                "An account with this email already exists but is not a superuser. "
                "Refusing to elevate it automatically."
            )

        User.objects.create_superuser(email=email, password=password, name=name)
        self.stdout.write("Bootstrap superuser created successfully.")
