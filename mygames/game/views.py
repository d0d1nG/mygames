from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from .forms import GameForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Max, Min, Count, Sum


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


# --=}_{==!|?|!==}_({=--  AGGREGATION  --=})_{==!|?|!==}_{=-- #


@login_required
def best(req):
    collection = Game.objects.all().aggregate(Max('grade'))
    maxVal = collection['grade__max']
    collection = Game.objects.all().filter(grade=maxVal)
    return render(req, 'aggreg_max_min.html', {'games': collection, 'grade': maxVal})


@login_required
def worst(req):
    collection = Game.objects.all().aggregate(Min('grade'))
    minVal = collection['grade__min']
    collection = Game.objects.all().filter(grade=minVal)
    return render(req, 'aggreg_max_min.html', {'games': collection, 'grade': minVal})


@login_required
def count(req):
    collection = Game.objects.all().aggregate(Count('grade'))
    avg = collection['grade__count']
    return render(req, 'aggreg_count.html', {'count': avg})


@login_required
def average(req):
    collection = Game.objects.all().aggregate(Avg('grade'))
    avg = collection['grade__avg']
    collection = Game.objects.count()
    return render(req, 'aggreg_avg.html', {'count': collection, 'average': avg})


@login_required
def summarize(req):
    collection = Game.objects.all().aggregate(Sum('grade'))
    sum = collection['grade__sum']
    collection = Game.objects.count()
    return render(req, 'aggreg_sum.html', {'count': collection, 'sum': sum})


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
            return redirect('demo_app:games')
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
            game = Game(title=form.cleaned_data['title'], comment=form.cleaned_data['comment'], release_year=form.cleaned_data['release_year'], reccomend=form.cleaned_data['would_recommend'], owner=req.user)
            game.save()
            return redirect('demo_app:games')
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
