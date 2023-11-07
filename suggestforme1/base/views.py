from django.shortcuts import render, redirect, get_object_or_404
from .models import userwatchedstatus,CustomUser,anime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from  .forms import SignUpForm
from django.db.models import Q

# Create your views here.
def home(request):
  animes=anime.objects.all()
  context={'animes':animes}
  return render(request,'base/home.html',context)

def suggestpage(request):
   return render(request,'base/home.html')
def animewatched(request, pk):
    animeobject = get_object_or_404(anime,name=pk)
    user = request.user
    user_view, created = userwatchedstatus.objects.get_or_create(user=user, anime=animeobject)
    user_view.viewed = True
    user_view.save()
    return redirect('animepage',pk=pk)

def animenotwatched(request, pk):
    animeobject = get_object_or_404(anime,name=pk)
    user = request.user
    user_view, created = userwatchedstatus.objects.get_or_create(user=user, anime=animeobject)
    user_view.delete()
    return redirect('animepage',pk=pk)



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['password1'] = form.cleaned_data['password1']
            request.session['email'] = form.cleaned_data['email']
            if form.cleaned_data['avatar']:
                    request.session['avatar'] = form.cleaned_data['avatar']
            else:
                    request.session['avatar'] = 'avatar.png'
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'base/signup.html', {'form': form})

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email OR password is incorrect')
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist")

    context = {'page': page}
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

from django.db.models import Q

def searchanime(request):
    cat = request.POST.get('cat')
    q = request.POST.get('q') if request.POST.get('q') else ''

    if cat == 'name':
        animes = anime.objects.filter(name__icontains=q)
    elif cat == 'genres':
        animes = anime.objects.filter(genres__icontains=q)
    elif cat == 'year':
        animes = anime.objects.filter(year__icontains=q)
    elif cat == 'format':
        animes = anime.objects.filter(format__icontains=q)
    elif cat == 'status':
        animes = anime.objects.filter(status__icontains=q)
    else:
        animes = anime.objects.filter(
            Q(name__icontains=q) |
            Q(genres__icontains=q) |
            Q(year__icontains=q) |
            Q(format__icontains=q)
        )

    watchedanimesobjects = userwatchedstatus.objects.filter(user=request.user)
    watchedanime = []

    for object in watchedanimesobjects:
        watchedanime.append(object.anime.name)

    animes = [anime for anime in animes if anime.name not in watchedanime]

    context = {'animes': animes, 'cat': cat}
    return render(request, 'base/searchanime.html', context)

def animepage(request, pk):
    animeobject= get_object_or_404(anime, name=pk)
    context = {'animeobject':animeobject}
    return render(request, 'base/animepage.html', context)