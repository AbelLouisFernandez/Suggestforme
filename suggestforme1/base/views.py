from django.shortcuts import render, redirect, get_object_or_404
from .models import userwatchedstatus,CustomUser,anime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from  .forms import SignUpForm

# Create your views here.
def home(request):
  animes=anime.objects.all()
  context={'animes':animes}
  return render(request,'base/home.html',context)

def suggestpage(request):
   return render(request,'base/home.html')
def mark_movie_viewed(request, movie_id):
    anime = get_object_or_404(anime, pk=movie_id)
    user = request.user
    user_view, created = userwatchedstatus.objects.get_or_create(user=user, anime=anime)
    user_view.viewed = True
    user_view.save()
    return redirect('movie_detail', movie_id=movie_id)



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