from django.shortcuts import render
from datetime import datetime, timedelta, timezone
from django.utils import timezone as djangotimezone
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from rest_framework import status
from Accounts.models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from Accounts.serializers import totalClientSerializer
# Create your views here.
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def sales_dashboard_details(request):
    user = request.user
    if user:
        # allPatients = User.objects.filter(patient=True).prefetch_related('customer_details', 'customer_details__referalId','customer_details__referalId__user')
        allPatients = CustomerDetails.objects.all()
        # allPatients = CustomerDetails.objects.filter(user__is_active=True).prefetch_related('referalId', 'referalId__user',)
        # total clients count
        total_patients_count = allPatients.count()
        # detials
        totalPatients = ClientDetialSerializer(allPatients, many=True)
        # time_threshold = datetime.datetime.now() - datetime.timedelta(days=1,hours=24)
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=24)


        

        # lastUpdatedPatientSerializer = CustomerLastUpdated24hoursSerilializer(lastUpdatedPatients, many=True)
    
        # total clients this month
        month = datetime.today().month
        this_month_patients = allPatients.filter(user__dateJoined__month=month)

        # details
        # this_month_patient_details = CustomerSerializer(this_month_patients, many=True)

        # this month count
        this_month_patients_count = this_month_patients.count()

    
        return JsonResponse({
            'firstname' : user.firstname,
            'lastname' : user.lastname,
            # 'lastUpdated_in_24Hours' : lastUpdatedPatientSerializer.data,   

            'total_patients_count' : total_patients_count,

            'this_month_patients_count' : this_month_patients_count,

            # details
            'totalPatients_details' : totalPatients.data
            # 'this_month_patient_details' : this_month_patient_details.data,
            # 'diet' : dietSerializer.data,
        })
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST','PATCH'])
@permission_classes((IsAuthenticated,))
def add_call_response(request):
    user = request.user
    response = request.data.get('response', None)
    customer = request.data.get('customer', None)
    date = request.data.get('date', None)
    note = request.data.get('note', None)  # Get the 'note' field from the request
    data = request.data.copy()

    if user.role == User.SALES:
        try:
            sales = SalesTeamDetails.objects.get(user=request.user.id)
        except SalesTeamDetails.DoesNotExist:
            return JsonResponse({"Error" : "Sales Team not found"}, status=status.HTTP_404_NOT_FOUND)

        data['sales'] = sales.id
        data['date'] = date if date is not None else  datetime.now().date()

        # Check if a duplicate entry exists for the given customer_id and date
        duplicates = CustomerCallReposnses.objects.filter(customer=customer, date=data['date'])
        if duplicates.count() > 0:
            # If a duplicate entry exists, delete it
            duplicates.delete()

        if request.method == 'PATCH':
            try:
                instance = CustomerCallReposnses.objects.get(customer=customer, date=datetime.today())
                serializer = CustomerCallReposnseSerializer(instance, data=data, partial=True)
            except CustomerCallReposnses.DoesNotExist:
                return JsonResponse({"error" : "call response not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CustomerCallReposnseSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Handle serializer validation errors

    return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_call_response(request):
    user = request.user
    customer = request.query_params.get('customer', None)
    param_date = request.query_params.get('date', None)
    date = param_date if param_date is not None else datetime.today()
    if user.role==User.SALES:
        if customer is not None:
            try:
                instance = CustomerCallReposnses.objects.get(customer=customer, date=date)
            except CustomerCallReposnses.DoesNotExist:
                return JsonResponse({'error' : 'no call repsonse'})
                # instance = ""
            serializer = CustomerCallReposnseSerializer(instance)
            return JsonResponse(serializer.data, safe=False)

        else:
            return JsonResponse({'error' : 'provide customer id in params'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_call_responses(request):
    user = request.user
    customer = request.query_params.get('customer', None)
    if user.role==User.SALES or user.role==User.DOCTOR:
        if customer is not None:
            responses = CustomerCallReposnses.objects.filter(customer=customer)
            serializer = CustomerCallReposnseSerializer(responses, many=True)
            return JsonResponse(serializer.data, safe=False)

        else:
            return JsonResponse({'error' : 'provide customer id in params'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def clients_this_month(request):
    user = request.user
    if user.role==User.SALES or user.role==User.ADMIN or user.role==User.CONSULTANT:

        # total clients this month
        month = datetime.today().month
        this_month_patients = CustomerDetails.objects.filter(user__dateJoined__month=month).prefetch_related('referalId', 'referalId__user')
        # details
        this_month_patient_details = ClientDetialSerializer(this_month_patients, many=True)
        return JsonResponse(this_month_patient_details.data, safe=False)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def no_update_clients(request):
    user = request.user
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=24)

    # lastUpdatedPatients = LastUpdateDate.objects.filter(Q(diet__lt = time_threshold) | Q(activity__lt = time_threshold) | Q(symptom__lt = time_threshold) | Q(medicine__lt = time_threshold)).prefetch_related('customer', 'customer__customer_details')
    if user.role==User.SALES:
        lastUpdatedPatients = CustomerDetails.objects.filter(
            Q(user__is_active__in=[True])

            & Q(user__last_update__activity__lt=time_threshold)
            & Q(user__last_update__symptom__lt=time_threshold)
            & Q(user__last_update__medicine__lt=time_threshold)).prefetch_related('user','referalId', 'referalId__user')

        # lastUpdatedPatientSerializer = CustomerLastUpdated24hoursSerilializer(lastUpdatedPatients, many=True)
        lastUpdatedPatientSerializer = ClientDetialSerializer(lastUpdatedPatients, many=True)
    
        return JsonResponse({
            'clients' : lastUpdatedPatientSerializer.data,
            'sales_firstname' : user.firstname,
            'sales_lastname' : user.lastname
        })
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def all_clients(request):
    user = request.user
    if user.role==User.SALES or user.role==User.DOCTOR or user.role==User.CONSULTANT:
        threshold_date = datetime.now().date() - timedelta(days=294) #42 weeks
        allClients = CustomerDetails.objects.filter(Menstruation_date__gte=threshold_date).prefetch_related('referalId', 'referalId__user')
        serializer = ClientDetialSerializer(allClients, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


from datetime import datetime
#this code is made by akash on 20/07/2023 for getting the api response as customer id and also with customer id and date together
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def sales_team_called_list(request):
    customer_id = request.query_params.get('customer_id', None)
    date_str = request.query_params.get('date', None)

    try:
        customer_id = int(customer_id)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid customer_id. Must be an integer.'},
                            status=status.HTTP_400_BAD_REQUEST)

    calls = CustomerCallReposnses.objects.filter(customer__id=customer_id)

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            calls = calls.filter(date=date)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Must be in YYYY-MM-DD format.'},
                                status=status.HTTP_400_BAD_REQUEST)

    if not calls.exists():
        return JsonResponse({'error': 'No calls found for the given customer_id and date combination.'},
                            status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerCallReposnsesSerializer(calls, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def clients_under_sales(request):
    user = request.user
    sales = request.query_params.get('sales', None)
    try:
        # sales = SalesTeamDetails.objects.get(user=sales)
        sales = User.objects.get(id=sales)
        sales = sales.salesDetails.first()
    except User.DoesNotExist:
        return JsonResponse({"Error" : "sales team not found"}, status=status.HTTP_404_NOT_FOUND)
    if user.role==User.ADMIN:
       
        CallResponse = CustomerCallReposnses.objects.filter(sales=user.id).distinct().values_list('customer')
        total_ids = list(CallResponse)

        clients = CustomerDetails.objects.filter(user__in=total_ids)
        serializer = totalClientSerializer(clients, many=True)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"Error" : "You dont have permission for that"}, status=status.HTTP_401_UNAUTHORIZED)

