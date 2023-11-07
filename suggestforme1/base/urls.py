from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[path('',views.home,name='home'),
             path('login/',views.loginPage, name='login'),
             path('logout/',views.logoutUser, name='logout'),
             path('signup/', views.signup, name='signup'),
             path('searchanime/',views.searchanime,name='searchanime'),
             path('animepage/<str:pk>/', views.animepage, name='animepage'),
             path('animepage/watched/<str:pk>', views.animewatched, name='animewatched'),
             path('animepage/not-watched/<str:pk>', views.animenotwatched, name='animenotwatched'),

              ]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)