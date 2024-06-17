from django.shortcuts import render,redirect
from ChatApp.models import Room,Message,ChatModelPvt
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout



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
    users = User.objects.exclude(username = request.user.username)
    return render(request,"one_to_one/Chat.html", {'users':users} )


#one to one message
def One_message(request,username):
    users = User.objects.exclude(username = request.user.username)
    user_obj = User.objects.get(username = username)
    
    print("users :",users)
    print("user_obj :",user_obj)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
        print('if thread_name :',thread_name)
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
        print('Else thread_name :',thread_name)
    message_objs =ChatModelPvt.objects.filter(thread_name=thread_name)
    return render(request,"one_to_one/One_to_one_message.html",{'users':users,'frnd':user_obj,'messages_': message_objs})



#login sign up
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
            messages.warning(request,"Username already existed")
            return render(request, 'signup.html')
        elif User.objects.filter(email=EMAIL).exists():
            messages.warning(request,"Email already Used")
            return redirect(Sign_Up)
        else:
            user = User.objects.create_user(username=USERNAME,email=EMAIL,password=PASSWORD)
            user.save()
            messages.success(request,'Account Created')
        return redirect(login_page)
    
#login views
def user_login(request):
    if request.method == "POST":
        USERNAME = request.POST.get('username')
        PASSWORD = request.POST.get('password')

        user = authenticate(username=USERNAME,password=PASSWORD)
        if user is not None:
            login(request, user)
            request.session['Username']=USERNAME
            request.session['Password']=PASSWORD
            messages.success(request,"Successfully logged in")
            return redirect(Chat_Page)
        else:
            return redirect(Home_page)
        


def logout_view(request):
    logout(request)
    messages.error(request,"Logout done")
    return redirect(Home_page)

# profile section 
def Profile_Page(request):
    data = User.objects.get(username=request.session['Username'])
    print(data)
    return render(request,"Profile.html",{'data':data})



