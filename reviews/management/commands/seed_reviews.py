import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models

class Command(BaseCommand):

    help = "this will create seeds for reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            help="how many reviews do you want to create"
        )
    
    def handle(self, *arg, **options):
        """
        create fake review data
        """
        number = int(options.get("number", 1))
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(review_models.Review, number, {
            'Accuracy': lambda x: random.randint(0,5),
            'communications': lambda x: random.randint(0,5),
            'cleanliness': lambda x: random.randint(0,5),
            'location': lambda x: random.randint(0,5),
            'check_in': lambda x: random.randint(0,5),
            'value': lambda x: random.randint(0,5),
            'user': lambda x: random.choice(users),
            'room': lambda x: random.choice(rooms)
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS("{} reviews CREATED".format(number)))
