import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

class Command(BaseCommand):

    help = "this will create seeds for reservation"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            help="how many reservations do you want to create"
        )
    
    def handle(self, *arg, **options):
        """
        create fake reservation data
        """
        number = int(options.get("number", 1))
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        cache = ""

        seeder.add_entity(reservation_models.Reservation, number, {
            "status": lambda x: random.choice(["pending", "canceled", "confirmed"]),
            'guest': lambda x: random.choice(users),
            'room':  lambda x: random.choice(rooms),
            "check_in": lambda x: generateTime(True),
            "check_out": lambda x: generateTime(False),
        })
        
        def generateTime(generate=True):
            global cache
            if generate:
                cache = datetime.now() + timedelta(days=random.randint(-50,50))
                return cache
            else:
                cache = cache + timedelta(days=random.randint(2,5))
                return cache

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("{} Reservation CREATED".format(number)))


