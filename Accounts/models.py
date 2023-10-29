from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.
from .validators import CheckIfAlpha
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone



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

class UserPostNatal(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('client', 'Client'),
        ('doctor', 'Doctor'),
        ('sales', 'Sales'),
        ('admin', 'Admin'),  # Added 'admin' role
    )
    role = models.CharField(max_length=10, choices=ROLES, default='client')
    email = models.EmailField(unique=True, max_length=300, default="example@email.com", blank=False)
    firstname = models.CharField(max_length=100, default="firstname")
    lastname = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    fcm_token = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Added is_staff field
    dateJoined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return f'{self.email} | {self.firstname}'

    objects = UserPostNatalManager()



class CustomerDetails(models.Model):
    user = models.OneToOneField(UserPostNatal, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, null=True)
    date_of_birth_parent = models.DateField(blank=True, null=True)
    babydob = models.DateField(null=True)
    profile_img = models.ImageField(upload_to='ProfilePic/', null=True, blank=True, default='/ProfilePic/default.jpg')
    babyGender = models.CharField(max_length=10, choices=(("male", "Male"), ("female", "Female")), null=True, blank=True)
    # Add any other fields you want to store for customers

    def __str__(self):
        return f'Customer Details for {self.user.email}'
    



