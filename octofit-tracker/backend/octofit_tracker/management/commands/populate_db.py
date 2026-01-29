from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data

        User = get_user_model()
        for obj in User.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Team.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Activity.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Leaderboard.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Workout.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()

        # Create Teams
        marvel = octo_models.Team.objects.create(name='Marvel')
        dc = octo_models.Team.objects.create(name='DC')

        # Create Users (super heroes)
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', team=marvel),
            User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='password', team=marvel),
            User.objects.create_user(username='batman', email='batman@dc.com', password='password', team=dc),
            User.objects.create_user(username='superman', email='superman@dc.com', password='password', team=dc),
        ]

        # Create Activities
        for user in users:
            octo_models.Activity.objects.create(user=user, type='run', duration=30, distance=5)
            octo_models.Activity.objects.create(user=user, type='cycle', duration=60, distance=20)

        # Create Workouts
        for user in users:
            octo_models.Workout.objects.create(user=user, name='Morning Cardio', description='Cardio session', duration=45)

        # Create Leaderboard
        for team in [marvel, dc]:
            octo_models.Leaderboard.objects.create(team=team, points=100)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
