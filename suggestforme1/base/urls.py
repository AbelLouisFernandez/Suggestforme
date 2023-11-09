from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns=[path('',views.home,name='home'),
             path('login/',views.loginPage, name='login'),
             path('logout/',views.logoutUser, name='logout'),
             path('signup/', views.signup, name='signup'),
             path('searchanime/',views.searchanime,name='searchanime'),
             path('animepage/<str:pk>/', views.animepage, name='animepage'),
             path('animepage/watched/<str:pk>', views.animewatched, name='animewatched'),
             path('animepage/not-watched/<str:pk>', views.animenotwatched, name='animenotwatched'),
             path('profile/',views.profile, name='profile'),
             path('reset_password/',views.custom_password_reset_view,name='password_reset'),
             path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='base/registration/password_reset_sent.html'),name='password_reset_done'), 
             path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='base/registration/password_reset_confirm.html'),name='password_reset_confirm'),
             path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='base/registration/password_reset_done.html'),name='password_reset_complete'),
 
              ]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)