from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=50)
    GAME_GENRE = [
        ('AC', 'Action'),
        ('AA', 'Action-adventure'),
        ('AD', 'Adventure'),
        ('RP', 'Role-Playing'),
        ('SI', 'Simulation'),
        ('ST', 'Strategy'),
        ('SP', 'Sports'),
        ('MM', 'MMO'),
        ('SB', 'Sandbox')
    ]
    genre = models.CharField(blank=True, choices=GAME_GENRE, max_length=2)
    release_year = models.IntegerField(blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    comment = models.TextField(help_text='your comment')
    grade = models.IntegerField(blank=True)
    would_recommend = models.BooleanField(default=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
