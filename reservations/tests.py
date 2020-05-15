from django.test import TestCase

import random
from datetime import datetime, timedelta
# Create your tests here.

class TimeGenerator():
    def __init__(self):
        self.time = datetime.now() + timedelta(days=random.randint(-50,50))
        print("init", self.time)

    def __str__(self):
        return str(self.time)

    def __call__(self):
        print(self.time)
        new_time = self.time + timedelta(days=3)
        print(new_time)
        return new_time

    def cache(self):
        return

time = TimeGenerator()

formated = {'time':lambda x: time.time()}
for i in range(3):
    print(formated['time']("a"))