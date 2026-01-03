from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.uploadImage, name='upload'),
    path('profile/<str:username>/', views.publicProfile, name='public_profile'),
]
