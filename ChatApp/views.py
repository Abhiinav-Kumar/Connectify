from django.shortcuts import render,redirect
from ChatApp.models import UserDB,Room,Message
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout

from ChatApp.forms import RegistrationForm, AccountAuthenticationForm
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

def Chat_Page(request,*args,**kwargs):
    return render(request,"one_to_one/Chat.html", )

def Sign_Up(request):
    return render(request,"SignUp.html")

def forgot_password(request):
    return render(request,"Password_managing/password_reset_form.html")


#registration view
def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            messages.warning(request, 'Account not found')
            return redirect(Chat_Page)

        else:
            context['registration_form'] = form

    return render(request,"SignUp.html")

def login_view(request,*args,**kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        messages.success(request,"Successfully signed")
        return redirect(Chat_Page)
    
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                messages.success(request,"Successfully login")
                return redirect(Chat_Page)
        else:
            context['login_form'] = form

    return render(request,"Signin.html")

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect= str(request.GET.get("next"))
    return redirect

def logout_view(request):
    logout(request)
    messages.error(request,"Logout done")
    return redirect(Home_page)

# profile section 
def Profile_Page(request):
    return render(request,"Profile.html",)

def account_view(request, *args ,**kwargs):

    context - {}
    

