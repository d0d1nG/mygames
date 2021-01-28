from django.urls import path
from . import views

app_name = 'demo_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.games, name='games'),
    path('game/<int:id>', views.game, name='game'),
    path('game/edit/<int:id>', views.edit, name='edit'),
    path('game/new/', views.new, name='new'),
    path('games/best/', views.best, name='best'),
    path('games/worst/', views.worst, name='worst'),
    path('games/average/', views.average, name='average'),
    path('games/count/', views.count, name='count'),
    path('games/summarize/', views.summarize, name='summarize'),
    path('signup/', views.signup, name='signup'),
]
