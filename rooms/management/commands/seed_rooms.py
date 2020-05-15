import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms.models import Room, RoomType
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
        create fake room data
        """
        number = int(options.get("number", 1))
        seeder = Seed.seeder()
        
        # never use all method when real time
        # it will make your computer super slow
        all_users = User.objects.all()
        room_types = RoomType.objects.all()
        seeder.add_entity(Room, number, {
            'name': lambda x: seeder.faker.address(),
            'host': lambda x: random.choice(all_users),
            'room_type': lambda x: random.choice(room_types),
            'price': lambda x: random.randint(0, 100000),
            'baths': lambda x: random.randint(0, 5),
            'bedrooms': lambda x: random.randint(0, 5),
            'beds': lambda x: random.randint(0, 5),
            'guests': lambda x: random.randint(0, 4),

        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS("{} Rooms CREATED".format(number)))
