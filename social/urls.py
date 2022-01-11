from django.urls import path
from . import views
urlpatterns = [
    
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
    path('profile/<str:pk>', views.userProfile, name='profile'),
    
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('room_form', views.createroom, name='createroom'),
    path('update_form/<str:pk>', views.updateroom, name='updateroom'),
    path('delete_form/<str:pk>', views.deleteroom, name='deleteroom')
]
