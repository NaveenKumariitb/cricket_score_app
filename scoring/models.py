from django.db import models

# Create your models here.

# scoring/models.py

from django.db import models
import uuid

class Player(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    image = models.ImageField(upload_to='player_images/')

    def __str__(self):
        return self.name

class Tournament(models.Model):
    tournament_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    players = models.ManyToManyField(Player, through='Match')

class Match(models.Model):
    match_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    runs_scored = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)
    is_out = models.BooleanField(default=False)
    balls_bowled = models.IntegerField(default=0)
    runs_conceded = models.IntegerField(default=0)
    wickets_taken = models.IntegerField(default=0)
    is_common_player = models.BooleanField(default=False)
    match_won = models.BooleanField(default=False)


