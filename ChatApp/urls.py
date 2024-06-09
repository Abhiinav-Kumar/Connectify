from django.urls import path
from ChatApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.Home_page,name='Home_page'),
    path('Chat_Page/',views.Chat_Page,name='Chat_Page'),

    # register view
    path('register_view/',views.register_view,name='register_view'),
    path('login_view/',views.login_view,name='login_view'),
    path('logout_view/',views.logout_view,name='logout_view'),


    path('Public_Room_page/',views.Public_Room_page,name='Public_Room_page'),
    path('MessageView/<str:room_name>/<str:username>',views.MessageView,name='MessageView'),


    path('Profile_Page/',views.Profile_Page,name='Profile_Page'),

    path('Sign_Up/',views.Sign_Up,name='Sign_Up'),
    
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
]