from django.urls import path
from ChatApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.Home_page,name='Home_page'),

    # one 2 one
    path('Chat_Page/',views.Chat_Page,name='Chat_Page'),
    path('<str:username>/<int:userid>',views.One_message,name='One_message'),

    # User Registration login logout
    path('Sign_Up/',views.Sign_Up,name='Sign_Up'),
    path('login_page/',views.login_page,name='login_page'),
    path('User_signup/',views.User_signup,name='User_signup'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout_view/',views.logout_view,name='logout_view'),


    # Room urls
    path('Public_Room_page/',views.Public_Room_page,name='Public_Room_page'),
    path('MessageView/<str:room_name>/<str:username>',views.MessageView,name='MessageView'),

    #profile
    path('Profile_Page/',views.Profile_Page,name='Profile_Page'),
    path('Profile_updation/<int:user_id>/',views.Profile_updation,name='Profile_updation'),
    path('Profile_update/<int:userid>/',views.Profile_update,name='Profile_update'),

    #update password
    path('Change_password/',views.Change_password,name='Change_password'),

    
    #Delete Acc
    path('DeleteAccount/',views.DeleteAccount,name='DeleteAccount'),


    #forgot password
    # path('forgot_password',views.forgot_password,name="forgot_password"),


    # forgot password in built
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_setups/password_reset_form.html'),name='password_reset'),

    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='password_setups/password_reset_done.html'),name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_setups/password_reset_confirm.html'),name='password_reset_confirm'),

    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name='password_setups/password_reset_complete.html'),name='password_reset_complete'),

    
]
