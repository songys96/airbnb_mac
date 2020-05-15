from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "it is command"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            help="how many"
        )

    def handle(self, *arg, **options):
        count = int(options.get("count"))
        for i in range(count):
            # 터미널에서 보이는 모습을 지정해 줄 수 있음
            self.stdout.write(self.style.SUCCESS("well-done"))