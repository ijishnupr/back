from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
from .validators import CheckIfAlpha


from django.contrib.auth.models import BaseUserManager

class UserPostNatalManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, firstname, lastname, password, **extra_fields)
class UserPostNatal(AbstractBaseUser,):
    email = models.EmailField(unique=True, max_length=300, default="example@email.com", blank=False)
    firstname = models.CharField(max_length=100, default="firstname", validators=[CheckIfAlpha])
    lastname = models.CharField(max_length=100, null=True, validators=[CheckIfAlpha])
    mobile = models.CharField(max_length=12, null=True, blank=True)
    babydob = models.DateField(null=True)  # Use DateField for 'babydob' as a date
    babyGender = models.CharField(max_length=10, choices=(("male", "Male"), ("female", "Female")), null=True, blank=True)
    fcm_token = models.TextField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='ProfilePic/', null=True, blank=True, default='/ProfilePic/default.jpg')
    is_active = models.BooleanField(default=True)
    dateJoined = models.DateTimeField(auto_now_add=True, editable=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return f'{self.email} | {self.firstname}'

    objects = UserPostNatalManager()