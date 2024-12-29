from django.shortcuts import render,redirect
from ChatApp.models import Room,Message,ChatModelPvt,User_details,NotificationDB
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
# Create your views here.

def Home_page(request):
    return render(request,"logins\Home.html")

#login sign up pages
def Sign_Up(request):
    return render(request,"logins\SignUp.html")

def login_page(req):
    return render(req,'logins\Signin.html')

#About us page
def about_us_page(request):
    return render(request,'about/about_us.html')

#registration view
def User_signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')

        EMAIL= email.strip()
        USERNAME = username.strip()
        PASSWORD = password.strip()

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
            user_details = User_details(user_name=USERNAME,user_id_id = user.id)
            user_details.save()
        return redirect(login_page)
    
#login views
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        USERNAME = username.strip()
        PASSWORD = password.strip()

        user = authenticate(username=USERNAME,password=PASSWORD)
        if user is not None:
            login(request, user)
            request.session['Username']=USERNAME
            request.session['Password']=PASSWORD
            
            messages.success(request,"Successfully logged in")
            return redirect(Chat_Page,)
        else:
            messages.error(request,"Username or Password is not matching, Try again")
            return redirect(login_page)
        

# logout view
def logout_view(request):
    logout(request)
    messages.success(request,"You have been successfully logged out")
    return redirect(Home_page)


# room message view
@login_required
def Public_Room_page(request):

    # getting user image for navbar
    current_user_id = request.user.id
    try:
        userdata = User_details.objects.get(user_id_id = current_user_id)
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
    

    
    return render(request,"rooms\Public_Room.html",{'userdata':userdata})


@login_required
def MessageView(request,room_name,username):

    # getting user image for navbar
    current_user_id = request.user.id
    try:
        userdata = User_details.objects.get(user_id_id = current_user_id)
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
    return render(request,"rooms\Message.html",context)
#end room message view




# Chat page views 
@login_required
def Chat_Page(request,*args,**kwargs):
    current_user_id = request.user.id

    loginedUser = User.objects.get(id=current_user_id)
    # print("Current user id :",current_user_id)
    users = User.objects.exclude(Q(id = current_user_id)| Q(username='default'))
    try:
        userdata = User_details.objects.get(user_id_id = current_user_id)

        #Getting users profile images
        users_data = []
        
        for user in users:
            try:
                user_img = User_details.objects.get(user_id_id = user.id )
            except User_details.DoesNotExist:
                user_img = User_details.objects.get(user_name='default')
            users_data.append({
                'user':user,
                'user_img':user_img
            })
        
    except User_details.DoesNotExist:
        userdata = User_details.objects.get(user_name='default')
        users_data =[]

    # notifications
    # notify = NotificationDB.objects.filter(receiver=current_user_id,is_read=False)
    unread_notifications = NotificationDB.objects.filter(receiver=current_user_id,is_read=False).values('sender').annotate(unread_count=Count('id'))

    notify = {item['sender']: item['unread_count'] for item in unread_notifications}
    # print("unread_notifications",notify)
    
        
    context = {'userdata':userdata,
               'users_data':users_data,
               'loginedUser':loginedUser,
               'notify':notify
               }

    return render(request,"one_to_one/Chat.html",context )


#one to one message view
@login_required
def One_message(request,username,userid):

    current_user_id = request.user.id
    users = User.objects.exclude(Q( id = current_user_id)| Q(username='default'))
    try:
        user_obj = User.objects.get(username = username)
    except User.DoesNotExist:
        return redirect(Chat_Page)
    
    #Getting user profile images for users tab
    users_data = []
    for user in users:
        try:
            user_img = User_details.objects.get(user_id_id = user.id)
        except User_details.DoesNotExist:
            user_img = User_details.objects.get(user_name='default')
        users_data.append({
            'user':user,
            'user_img':user_img
        })

    # getting image for chat tab
    try:
        userpro =User_details.objects.get(user_id_id=userid)
        userdata = User_details.objects.get(user_id_id = current_user_id)
    except User_details.DoesNotExist:
        userdata = User_details.objects.get(user_name="default")
        userpro = User_details.objects.get(user_name="default")
    
        
    # Determine the thread_name based on user IDs to fetch messages
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
        # print('if thread_name :',thread_name)
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
        # print('Else thread_name :',thread_name)

    message_objs =ChatModelPvt.objects.filter(thread_name=thread_name)

    # notification view 
    unread_notifications = NotificationDB.objects.filter(receiver=current_user_id,is_read=False).values('sender').annotate(unread_count=Count('id'))
    notify = {item['sender']: item['unread_count'] for item in unread_notifications}
    # print("unread_notifications",notify)
    NotificationDB.objects.filter(roomname=thread_name,receiver=request.user.id).update(is_read=True)

    context ={
        'users':users,
        'frnd':user_obj,
        'messages_data': message_objs,
        'userpro':userpro,
        'userdata':userdata,
        'users_data':users_data,
        'notify':notify

    }

    return render(request,"one_to_one/One_to_one_message.html",context)




# profile section 
@login_required
def Profile_Page(request):
    current_user_id = request.user.id
    try:
        data = User.objects.get(id=current_user_id)
        userdata = User_details.objects.get(user_id_id =current_user_id)
        
    except User.DoesNotExist:
        return redirect(Home_page)
    return render(request,"profile/Profile.html",{'data':data,'userdata':userdata})   


# profile Updation
@login_required
def Profile_updation(request,user_id):
    
    data = User.objects.get(id=user_id)
    userdata = User_details.objects.get(user_id_id=user_id)
    return render(request,"profile/Profile_update.html",{'userdata':userdata,'data':data})

@login_required
def Profile_update(request,userid):
    if request.method == "POST":
        us = request.POST.get('username')
        em = request.POST.get('email')
        BIO = request.POST.get('bio')
                
        US = us.strip()
        EM = em.strip()
        existing_user = User.objects.filter(Q(username=US) | Q(email=EM)).exclude(id=userid).exists()

        if existing_user:
            messages.warning(request, "Username or email already exists. Please choose another.")
            data = User.objects.get(id=userid)
            userdata = User_details.objects.get(user_id_id=userid)
            return render(request, 'profile/Profile_update.html',{'userdata':userdata,'data':data})
         
        try:
            PROIMG = request.FILES['profile-image']
            fs = FileSystemStorage()
            file = fs.save(PROIMG.name,PROIMG)
        except MultiValueDictKeyError:
            file = User_details.objects.get(user_id_id =userid).profile_image
        User_details.objects.filter(user_id_id=userid).update(Bio=BIO,profile_image=file)
        User.objects.filter(id=userid).update(email=EM,username=US)
        messages.success(request,"Your profile has been updated successfully!")
        return redirect(Profile_Page)
    
#Update Password
def Change_password(request):

    if request.method == "POST":
        obj = PasswordChangeForm(user=request.user,data=request.POST)
        print(obj)
        if obj.is_valid():
            obj.save()
            update_session_auth_hash(request,obj.user)
            messages.success(request,"Your password has been updated successfully!")
            return redirect(Profile_Page)
    else:
        obj = PasswordChangeForm(user=request.user)
    return render(request,"profile/Change_password.html",{'obj':obj})



#Delete Account
@login_required
def DeleteAccount(request):
    if request.method == "POST":
        Apass = request.POST.get('acc-password')
        Auser = request.POST.get('acc-username')

        user = authenticate(username=Auser, password=Apass)
        if user is not None:
            user.delete()
            messages.error(request,"Your account has been deleted successfully. We're sorry to see you go.")
            return redirect('Home_page')  
        else:
            messages.warning(request,"wrong password ")
            return redirect('Profile_Page')  
        


