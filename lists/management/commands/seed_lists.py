import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

class Command(BaseCommand):

    help = "this will create seeds for lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            help="how many lists do you want to create"
        )
    
    def handle(self, *arg, **options):
        """
        create fake list data
        """
        number = int(options.get("number", 1))
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(list_models.List, number, {
            'user': lambda x: random.choice(users),
        })
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = random.choices(rooms, k=random.randint(5,10))
            list_model.rooms.add(*to_add)
            # to_add 와 *to_add 의 차이점
            # to_add는 쿼리셋을 반환하고 *to_add는 쿼리 안의 요소를 꺼내서 반환한다

        self.stdout.write(self.style.SUCCESS("{} Lists CREATED".format(number)))
