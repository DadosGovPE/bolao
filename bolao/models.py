from django.contrib.auth.models import User
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    team1 = models.ForeignKey(Team, related_name='team1_games', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_games', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.date}"

class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game} - {self.team1_score}:{self.team2_score}"
