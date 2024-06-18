from django.shortcuts import render,redirect
from ChatApp.models import Room,Message,ChatModelPvt,User_details
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
# Create your views here.

def Home_page(request):
    return render(request,"Home.html")

#login sign up pages
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
            messages.error(request,"Username or Password is not matching, Try again")
            return redirect(login_page)
        

# logout view
def logout_view(request):
    logout(request)
    messages.error(request,"Logout done")
    return redirect(Home_page)




# room message view
def Public_Room_page(request):

    try:
        userdata = User_details.objects.get(user_name=request.user.username)
    except User_details.DoesNotExist:
        userdata = User_details.objects.get(user_name="default")


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

    return render(request,"Public_Room.html",{'userdata':userdata})

def MessageView(request,room_name,username):

    try:
        userdata = User_details.objects.get(user_name=request.user.username)
    except User_details.DoesNotExist:
        userdata = User_details.objects.get(user_name="default")

    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
        'userdata':userdata
    }
    return render(request,"Message.html",context)
#end room message view



# Main page views 
def Chat_Page(request,*args,**kwargs):

    try:
        users = User.objects.exclude(Q(username = request.user.username)| Q(username='default'))
        userdata = User_details.objects.get(user_name = request.user.username)

        #Getting user profile images
        users_data = []
        for user in users:
            try:
                user_img = User_details.objects.get(user_name=user)
            except User_details.DoesNotExist:
                user_img = User_details.objects.get(user_name='default')
        
    except User_details.DoesNotExist:
        userdata = User_details.objects.get(user_name='default')
    return render(request,"one_to_one/Chat.html", {'users':users,'userdata':userdata} )



#one to one message view
def One_message(request,username):
    users = User.objects.exclude(username = request.user.username)
    user_obj = User.objects.get(username = username)
    

    try:
        userpro =User_details.objects.get(user_name=username)
        userdata = User_details.objects.get(user_name=request.user.username)
    except User_details.DoesNotExist:
        userpro = User_details.objects.get(user_name="default")
        userdata = User_details.objects.get(user_name="default")

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
        print('if thread_name :',thread_name)
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
        print('Else thread_name :',thread_name)
    message_objs =ChatModelPvt.objects.filter(thread_name=thread_name)
    return render(request,"one_to_one/One_to_one_message.html",{'users':users,'frnd':user_obj,'messages_': message_objs,'userpro':userpro,'userdata':userdata})




# profile section 
def Profile_Page(request):
    try:
        data = User.objects.get(username=request.session['Username'])
        userdata = User_details.objects.get(user_name=request.session['Username'])
        
    except User_details.DoesNotExist:
        userdata = User_details.objects.get(user_name="default")
    return render(request,"Profile.html",{'data':data,'userdata':userdata})   



