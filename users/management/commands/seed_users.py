from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

class Command(BaseCommand):

    help = "this will create seeds for users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            help="how many users do you want to create"
        )
    
    def handle(self, *arg, **options):
        """
        create fake user data
        we will control user's auth
        is_superuser(PermissionMixin), is_staff(AbstractUser) should be False
        otherwise they can see other's information
        """
        number = int(options.get("number", 1))
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {
            'is_staff':False,
            'is_superuser':False
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS("{} Users CREATED".format(number)))
