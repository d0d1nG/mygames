from django.forms import ModelForm
from .models import Game, Review


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'genre', 'release_year']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'grade', 'would_recommend']
