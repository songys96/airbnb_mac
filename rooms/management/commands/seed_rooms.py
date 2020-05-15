import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms.models import Room, RoomType, Photo, Amenity, Facility, HouseRule
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

        # from now, we admin room details on room which created above
        created_photos = seeder.execute()
        # django.contrib.admin.utils import flatten
        # flatten = 반음 낮추다, 단조롭게 하다.
        created_clean = flatten(list(created_photos.values()))
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        rules = HouseRule.objects.all()

        for pk in created_clean:
            room = Room.objects.get(pk=pk)

            # 기존에 없는 사진을 room과 foreignKey로 연결하여 저장
            for i in range(random.randint(4,6)):
                Photo.objects.create(
                    caption = seeder.faker.sentence(),
                    file = "/room_photos/{}.jpeg".format(random.randint(1,12)),
                    room = room
                )
            # 기존에 있는 amenities를 등록
            for a in amenities:
                magic_number = random.randint(0,15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0,15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in rules:
                magic_number = random.randint(0,15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

                
        self.stdout.write(self.style.SUCCESS("{} Rooms CREATED".format(number)))
