from django.shortcuts import render, redirect, get_object_or_404
from .models import userwatchedstatus,CustomUser,anime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from  .forms import SignUpForm
from django.db.models import Q
import random
from django.contrib.auth.views import PasswordResetView
from django_ratelimit.decorators import ratelimit
from verify_email.email_handler import send_verification_email

# Create your views here.
def home(request):
  animes=anime.objects.all()
  if request.user.is_authenticated:
        watchedanimesobjects = userwatchedstatus.objects.filter(user=request.user)
        watchedanime = []
        for object in watchedanimesobjects:
              if object.viewed==True:
                  watchedanime.append(object.anime.name)
        animes = [anime for anime in animes if anime.name not in watchedanime]
  else:
      animes=[anime for anime in animes]
  random.shuffle(animes)
  context={'animes':animes}
  return render(request,'base/home.html',context)
def profile(request):
    user=request.user
    animes=anime.objects.all()
    watchedanimesobjects = userwatchedstatus.objects.filter(user=request.user)
    watchedanime = []
    for object in watchedanimesobjects:
        if object.viewed==True:
            watchedanime.append(object.anime.name)
    animes = [anime for anime in animes if anime.name in watchedanime]
    context={'user':user,'animes':animes}
    return render(request,'base/profile.html',context)

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
    user_view= userwatchedstatus.objects.get(user=user, anime=animeobject)
    user_view.viewed = False
    user_view.save()
    return redirect('animepage',pk=pk)



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            enteredemail=form.cleaned_data['email']
            users=CustomUser.objects.get(email=enteredemail)
            if users:
                messages.error(request, 'This email has already been registered to a user')
            else:
                if form.cleaned_data['avatar']:
                    pass
                else:
                    form.cleaned_data['avatar']='avatar.png'
                    inactive_user = send_verification_email(request, form)
                    return render(request,'base/verificationemailsent.html')
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
    elif cat == 'startyear':
        animes = anime.objects.filter(startyear__icontains=q)
    elif cat == 'format':
        animes = anime.objects.filter(format__icontains=q)
    elif cat == 'status':
        animes = anime.objects.filter(status__icontains=q)
    else:
        animes = anime.objects.filter(
            Q(name__icontains=q) |
            Q(genres__icontains=q) |
            Q(startyear__icontains=q) |
            Q(format__icontains=q)
        )
    if request.user.is_authenticated:
            watchedanimesobjects = userwatchedstatus.objects.filter(user=request.user)
            watchedanime = []

            for object in watchedanimesobjects:
                if object.viewed==True:
                    watchedanime.append(object.anime.name)

            animes = [anime for anime in animes if anime.name not in watchedanime]
    context = {'animes': animes, 'cat': cat}
    return render(request, 'base/searchanime.html', context)

def animepage(request, pk):
    animeobject= get_object_or_404(anime, name=pk)
    user = request.user
    if request.user.is_authenticated:
        user_view = userwatchedstatus.objects.get_or_create(user=user, anime=animeobject) 
    else:
        user_view=[]
    context = {'animeobject':animeobject,'user_view':user_view}
    return render(request, 'base/animepage.html', context)

def handler500(exception):
    response = render(exception,template_name='base/404.html')
    response.status_code = 500
    return response
def handler400(request, exception):
    response = render(request,template_name='base/404.html')
    response.status_code = 400
    return response
def handler404(request, exception):
    response = render(request,template_name='base/404.html')
    response.status_code = 400
    return response
class CustomPasswordResetView(PasswordResetView):
    template_name='base/registration/password_reset.html'
    email_template_name = 'base/registration/password_reset_email.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data['email']
        self.extra_context = {'email': email}
        return response

@ratelimit(key='ip', rate='2/h', method='POST')  # if users are behind a shared IP (such as in some corporate or public networks)
def custom_password_reset_view(request, *args, **kwargs):
    return CustomPasswordResetView.as_view()(request, *args, **kwargs)