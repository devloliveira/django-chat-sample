from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Inserts some users so we can play around with the app'

    def add_arguments(self, parser):
        # No need for additional arguments for this command.
        pass

    def handle(self, *args, **options):

        # First let us delete all users created so far.
        self._cleanup_db()

        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all previous users')
        )

        # Now let us create some users
        self._create_default_users()

        self.stdout.write(
            self.style.SUCCESS('Successfully created the users')
        )

    def _cleanup_db(self):
        for user in User.objects.all():
            user.delete()

    def _create_default_users(self):
        default_users_data = (
            ('leonardo', 'a@a.com', '123'),
            ('maria', 'b@b.com', '123'),
            ('john', 'c@c.com', '123'),
        )

        for user_data in default_users_data:
            self._create_user(*user_data)

    def _create_user(self, username, email, password):
        return User.objects.create_user(username, email, password)
