from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_release_year(value):
    if 1950 > value > 2021:
        return ValidationError('That year is not valid')
    else:
        return value


def validate_grade(value):
    if 0 > value > 10:
        return ValidationError('Your grade is not valid, please use values from 0 to 10')
    else:
        return value


class Game(models.Model):
    title = models.CharField(max_length=50, default='')
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
    genre = models.CharField(blank=True, choices=GAME_GENRE, max_length=2, default='')
    release_year = models.IntegerField(blank=True, validators=[validate_release_year])
    comment = models.TextField(help_text='your comment', default='')
    grade = models.IntegerField(default=0, validators=[validate_grade])
    would_recommend = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.title
