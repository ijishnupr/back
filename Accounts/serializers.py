from rest_framework import serializers
from .models import *
from payment.models import *
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site


class UserPostNatalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'mobile', 'fcm_token','password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CustomerDetailsSerializer(serializers.ModelSerializer):
    # Add a new field for first name, and use 'source' to point to the related User's first name
    first_name = serializers.CharField(source='user.firstname', read_only=True)

    class Meta:
        model = CustomerDetails
        fields = ['id', 'address', 'date_of_birth_parent', 'babydob', 'profile_img', 'babyGender', 'user', 'doctor_referal', 'first_name']




from rest_framework.validators import UniqueValidator

class DoctorRegistrationSerializer(serializers.Serializer):
    # User registration fields
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    firstname = serializers.CharField(max_length=100, required=True)
    lastname = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    # Doctor-specific fields
    speciality = serializers.CharField(max_length=200, required=True)
    qualification = serializers.CharField(max_length=200, required=True)
    medicalCouncil = serializers.CharField(max_length=20, required=True)
    councilRegNo = serializers.CharField(max_length=200, required=True)
    hospitals = serializers.CharField(max_length=300, required=True)
    interests = serializers.CharField(max_length=200, required=True)
    placeOfWork = serializers.CharField(max_length=200, required=True)
    onlineConsultation = serializers.CharField(max_length=100, required=True)
    experience = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=True)
    languages = serializers.CharField(max_length=500, required=False)
    location = serializers.CharField(max_length=200, required=False, allow_blank=True)
    referalId = serializers.CharField(max_length=100, required=False, allow_blank=True)
    price = serializers.IntegerField(required=False)
    gender = serializers.ChoiceField(choices=DoctorDetails.GENDER_CHOICES, required=False, allow_blank=True)


class SalesTeamRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    firstname = serializers.CharField()
    lastname = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField()

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        firstname = validated_data['firstname']
        lastname = validated_data.get('lastname', '')
        location = validated_data['location']

        # Create the user with the SALES role
        user = User.objects.create_user(email=email, password=password, role=4, firstname=firstname, lastname=lastname)

        # Create SalesTeamDetails
        SalesTeamDetails.objects.create(user=user, location=location)

        return user
    

class ConsultantTeamRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    firstname = serializers.CharField()
    lastname = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField()

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        firstname = validated_data['firstname']
        lastname = validated_data.get('lastname', '')
        location = validated_data['location']

        # Create the user with the CONSULTANT role
        user = User.objects.create_user(email=email, password=password, role=5, firstname=firstname, lastname=lastname)

        # Create ConsultantInfo
        ConsultantInfo.objects.create(user=user, location=location)

        return user


class DoctorDetailSerializer(serializers.ModelSerializer):
    accountStatus = serializers.BooleanField(source='user.is_active')
    
    

    # new
    id = serializers.CharField(source='user.id')
    firstname = serializers.CharField(source='user.firstname')
    lastname = serializers.CharField(source='user.lastname')
    email = serializers.CharField(source='user.email')
    



    class Meta:
        model = DoctorDetails
        fields = ['id' ,'firstname', 'hospitals','lastname', 'email', 'age', 'location', 'councilRegNo', 'experience','qualification','speciality', 'accountStatus', 'price', 'gender', 'languages', 'referalId',]


# admin serializers
from django.db.models import Prefetch
   

class totalClientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    email = serializers.CharField(source='user.email')
    firstname = serializers.CharField(source='user.firstname')
    lastname = serializers.CharField(source='user.lastname')
    dateJoined = serializers.DateTimeField(source='user.dateJoined')
    subscription = serializers.SerializerMethodField()
  
    doctor_firstname = serializers.CharField(source='referalId.user.firstname', required=False)
    doctor_lastname = serializers.CharField(source='referalId.user.lastname', required=False)
    is_active = serializers.BooleanField(source='user.is_active')
   
    profile_pic = serializers.ImageField(source="user.profile_img")
    
    class Meta:
        model = CustomerDetails
        fields = ['id', 'firstname', 'lastname', 'email', 'dateJoined', 'doctor_firstname', 'doctor_lastname', 'is_active','subscription', 'profile_pic']

    

    

    def get_subscription(self, obj):
        membership = PurchasedMembership.objects.filter(user = obj.user,is_paid = True).order_by('-pk')


        if membership.exists():
            return membership[0].membership.membership_name
        
                   
        return "No plans"
        


    @staticmethod
    def pre_loader(queryset):
        queryset = queryset.prefetch_related(
            'user',
            'doctor_referal',
          
            Prefetch("user__sub_client", queryset=Subscriptions.objects.filter(is_active=True).prefetch_related('membership'))
        )
        return queryset
    
class adminDashboardCountsSerializer(serializers.Serializer):
    totalConsultant = serializers.IntegerField()
    totalSalesTeam = serializers.IntegerField()
    activeClients = serializers.IntegerField()
    disabledDoctors = serializers.IntegerField()
    totalDoctors = serializers.IntegerField()
    totalClients = serializers.IntegerField()

class SalesTeamSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='user.id')
    firstname = serializers.CharField(source='user.firstname')
    email = serializers.EmailField(source='user.email')
    accountStatus = serializers.BooleanField(source='user.is_active')
    password = serializers.CharField(source='passwordString')

    class Meta:
        model = SalesTeamDetails 
        fields = '__all__'
        extra_kwargs = {
            'passwordString' : {'write_only' : True},
            'user' : {'write_only' : True},
        }


class ConsultantInfoSerializer(serializers.ModelSerializer):
    accountStatus = serializers.BooleanField(source='user.is_active', read_only=True)
    name = serializers.CharField(source='user.firstname', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    profile_pic = serializers.SerializerMethodField()
    
    class Meta:
        model = ConsultantInfo
        fields = ['name', 'email', 'location', 'passwordString', 'accountStatus','user', 'profile_pic']

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        if obj.user.profile_img:
            return "https://" + str(get_current_site(request)) + "/media/" + str(obj.user.profile_img)
        else:
            return "https://" + str(get_current_site(request)) + "/media/ProfilePic/" + str("default.jpg")



class RegistrationSerializers(serializers.ModelSerializer):
    id = serializers.CharField( read_only=True)
    password2 = serializers.CharField(style={'input_type':'passsword'}, write_only=True, required=False)
    firstname = serializers.CharField(required=True)
    email = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all(),message="An account with this email already exists")])
    profile_pic = serializers.SerializerMethodField(read_only=True)
    fcm_token = serializers.CharField(allow_blank=True, required=False)
    



    class Meta:
        model = User
        fields = ['email', 'firstname', 'lastname', 'mobile', 'password', 'password2','id','profile_pic','role','fcm_token']
        extra_kwargs = {
            'password' : {'write_only':True},
            'lastname': {'required': True},
            'mobile': {'required': True},
            'role': {'required': True},
        }

    def save(self):
        password = self.validated_data.get('password', None)
        password2 = self.validated_data.get('password2', None)
        email = self.validated_data.get('email',None)
        firstname = self.validated_data.get('firstname', None)
        lastname = self.validated_data.get('lastname', None)
        mobile = self.validated_data.get('mobile', None)
        role = self.validated_data.get('role', None)
 
       
        if email is not None:
            email = email.lower()
            if role == User.CLIENT:
                user = User.objects.create_patient(email=email,password=password, firstname=firstname, lastname=lastname, mobile=mobile)
        
            elif role == User.DOCTOR:
                user = User.objects.create_doctor(email=email,password=password, firstname=firstname, lastname=lastname, mobile=mobile)                
            elif role == User.SALES:
                user = User.objects.create_sales(email=email,password=password, firstname=firstname)
            elif role == User.CONSULTANT:
                user = User.objects.create_consultant(email=email,password=password, firstname=firstname)
            elif role == User.HOSPITAL_MANAGER:
                user = User.objects.create_hospitalManager(email=email,password=password, firstname=firstname)
            else:
                raise serializers.ValidationError({'Error':'User type not defined'})
            return user

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("An account with this email already exists")
        return lower_email

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        try:
            return "https://" + str(get_current_site(request)) + "/media/" + str(obj.profile_img)
        except:
            return "https://" + str(get_current_site(request)) + "/media/ProfilePic/" + str("default.jpg")
