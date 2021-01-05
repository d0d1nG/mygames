from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from .forms import GameForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def index(req):
    if not req.user.is_authenticated:
        return render(req, 'index.html', {'page_title': 'Home Page'})
    else:
        return redirect('demo_app:games')


@login_required
def games(req):
    collection = Game.objects.all()
    return render(req, 'games.html', {'games': collection})


@login_required
def game(req, id):
    # gobject : game_object
    gobject = get_object_or_404(Game, id=id)
    return render(req, 'game.html', {'game': gobject, 'page_title': gobject.title})


@permission_required('game.change_game')
def edit(req, id):
    if req.method == 'POST':
        form = GameForm(req.POST)

        if form.is_valid():
            game = Game.objects.get(id=id)
            game.title = form.cleaned_data['title']
            game.comment = form.cleaned_data['comment']
            game.release_year = form.cleaned_data['release_year']
            game.would_recommend = form.cleaned_data['would_recommend']
            game.save()
            return redirect('game:games')
        else:
            return render(req, 'edit.html', {'form': form, 'id': id})
    else:
        game = Game.objects.get(id=id)
        form = GameForm(instance=game)
        return render(req, 'edit.html', {'form': form, 'id': id})


@permission_required('game.add_game')
def new(req):
    if req.method == 'POST':
        form = GameForm(req.POST)

        if form.is_valid():
            game = Game(title=form.cleaned_data['title'], release_year=form.cleaned_data['release_year'], reccomend=form.cleaned_data['would_recommend'], owner=req.user)
            game.save()
            return redirect('game:games')
        else:
            return render(req, 'new.html', {'form': form})
    else:
        form = GameForm()
        return render(req, 'new.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()
            login(request, user)
            return redirect('demo_app:games')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
