from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager



#create a new user
#create a superuser

class MyAccountManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            email=self.normalize_email(email), #to make email to lowercase
            username=username,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin  =True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



def get_profile_image_filepath(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_dafault_profile_image():
    return "logo/Connectify.png"


class UserDB(AbstractBaseUser):

    email         = models.EmailField(verbose_name="email",null=True,blank=True,max_length=100,unique=True)
    username      = models.CharField(max_length=30,null=True,blank=True,unique=True)
    date_joined   = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login    = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)
    Profile_image = models.ImageField(upload_to=get_profile_image_filepath,null=True,blank=True,default=get_dafault_profile_image)
    hide_email    = models.BooleanField(default=True)
    password      = models.CharField(max_length=128) 

    objects =MyAccountManager()

    USERNAME_FIELD = 'email'                        #if you want login with email as supposed to the username
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username if self.username else "No Username"
    
    # rename profile image to profile_image.png
    def get_profile_image_filename(self):
        return str(self.Profile_image)[str(self.Profile_image).index(f'profile_iamge/{self.pk}'):]
    
    # default permission that are with the abstract base user class
    def has_perm(self,perm,obj=None):  
        return self.is_admin
    
    # module permission 
    def has_module_perms(self,app_label):
        return True

    



#public chat room model

class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name

    def return_room_messages(self):
        return Message.objects.filter(room=self)

    def create_new_room_message(self, sender, message):
        new_message = Message(room=self, sender=sender, message=message)
        new_message.save()


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return str(self.room)

