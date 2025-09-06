from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create authentication tokens for all existing users'

    def handle(self, *args, **options):
        users_without_tokens = User.objects.filter(auth_token__isnull=True)
        
        for user in users_without_tokens:
            token = Token.objects.create(user=user)
            self.stdout.write(
                self.style.SUCCESS(f'Created token for user: {user.username} - Token: {token.key}')
            )
        
        if not users_without_tokens.exists():
            self.stdout.write(
                self.style.WARNING('All users already have tokens')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Total users with tokens: {User.objects.filter(auth_token__isnull=False).count()}')
        )