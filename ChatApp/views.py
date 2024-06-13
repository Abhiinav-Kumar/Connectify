from django.shortcuts import render,redirect
from ChatApp.models import Room,Message
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login



# Create your views here.

def Home_page(request):
    return render(request,"Home.html")


# room message view
def Public_Room_page(request):
    if request.method == "POST":
        username = request.POST['username']
        room = request.POST['room_name']

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect(MessageView,room_name=room,username=username)
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()

        return redirect('MessageView',room_name=room,username=username)

    return render(request,"Public_Room.html")

def MessageView(request,room_name,username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,

    }
    return render(request,"Message.html",context)
#end room message view

#page views
def Chat_Page(request,*args,**kwargs):
    return render(request,"one_to_one/Chat.html", )

def Sign_Up(request):
    return render(request,"SignUp.html")

def login_page(req):
    return render(req,'Signin.html')

def forgot_password(request):
    return render(request,"Password_managing/password_reset_form.html")


#registration view
def User_signup(request):
    if request.method == "POST":
        EMAIL = request.POST.get('email')
        USERNAME = request.POST.get('username')
        PASSWORD = request.POST.get('password1')

        if User.objects.filter(username=USERNAME).exists():
            # Handle duplicate username (e.g., display error message)
            return render(request, 'signup.html', {'messages': 'Username already exists'})
        else:
            user = User.objects.create_user(username=USERNAME,email=EMAIL,password=PASSWORD)
            user.save()
        return redirect(request,login_page)
    
#login views

def user_login(request):
    if request.method == "POST":
        USERNAME = request.POST.get('username')
        PASSWORD = request.POST.get('password')

        user = authenticate(username=USERNAME,password=PASSWORD)
        if user is not None:
            login(request, user)
            return redirect(request,Chat_Page)
        else:
            return redirect(request,Home_page)





def logout_view(request):
    logout(request)
    messages.error(request,"Logout done")
    return redirect(Home_page)

# profile section 
def Profile_Page(request):
    return render(request,"Profile.html",)



