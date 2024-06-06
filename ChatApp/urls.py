from django.urls import path
from ChatApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.Home_page,name='Home_page'),
    path('Chat_Page/',views.Chat_Page,name='Chat_Page'),

    path('Public_Room_page/',views.Public_Room_page,name='Public_Room_page'),
    path('MessageView/<str:room_name>/<str:username>',views.MessageView,name='MessageView'),


    path('Profile_Page/',views.Profile_Page,name='Profile_Page'),

    path('Sign_Up/',views.Sign_Up,name='Sign_Up'),
    path('save_Sign_up/',views.save_Sign_up,name='save_Sign_up'),

    path('Sign_in/',views.Sign_in,name='Sign_in'),
    path('Login_user/',views.Login_user,name='Login_user'),

    path('User_logout/',views.User_logout,name='User_logout'),

    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
]