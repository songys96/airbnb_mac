from django.core.management.base import BaseCommand
from rooms.models import Amenity

class Command(BaseCommand):

    help = "this will create seeds for amenities"

    def handle(self, *arg, **options):
        amenities = [
            "Air Conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Boating",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Oven",
            "Outdoor Pool",
            "Queen Size Bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Sofa"
        ]
        
        for a in amenities:
            Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenities are created"))
        
        # above will work as below
        #a = Amenity()
        #a.name = "WahsingMachine"
        #a.save()
    """  
    # this is not neccessary in here     
    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            help="how many"
        )
    """