from django.core.management.base import BaseCommand
from rooms.models import Facility

class Command(BaseCommand):

    help = "this will create seeds for facilities"

    def handle(self, *arg, **options):
        facilities = [
            "Private entrance",
            "Paid Parking on Premise",
            "Paid Parking off Premise",
            "Elevator",
            "Parking",
            "Gym"
        ]

        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("facilities are created"))
        
        
    """  
    # this is not neccessary in here     
    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            help="how many"
        )
    """