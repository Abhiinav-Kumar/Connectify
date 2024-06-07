from django.shortcuts import render,redirect
from ChatApp.models import UserDB,Room,Message
from django.contrib import messages

# Create your views here.
def Home_page(request):
    return render(request,"Home.html")

def Chat_Page(request,*args,**kwargs):
    context = {}
    return render(request,"one_to_one/Chat.html", context ) 


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


def Profile_Page(request):
    return render(request,"Profile.html",)

def Sign_Up(request):
    return render(request,"SignUp.html")

def save_Sign_up(request):
    if request.method == "POST":
        email = request.POST.get('EMAIL')
        user = request.POST.get('USERNAME')
        pwd = request.POST.get('PASSWORD')

        if UserDB.objects.filter(Email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'SignUp.html',)

        elif UserDB.objects.filter(Username=user).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'SignUp.html',)
        else:
            obj = UserDB(Email=email,Username=user,Password=pwd)
            obj.save()
            messages.success(request, 'Account created successfully')
            return redirect(Sign_in)

    return render(request, 'Sign_Up.html')


def Sign_in(request):
    return render(request,"Signin.html")


def Login_user(request):
    if request.method == 'POST':
        user = request.POST.get('USERNAME')
        pwd = request.POST.get('PASSWORD')

        if UserDB.objects.filter(Username=user).exists():
            return redirect(Chat_Page)
        else:
            messages.warning(request, 'Account not found')
            return redirect(Sign_in)
    else:
        messages.warning(request, 'Account not found')
        return redirect(Sign_in)

def User_logout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(Home_page)

def forgot_password(request):
    return render(request,"Password_managing/password_reset_form.html")