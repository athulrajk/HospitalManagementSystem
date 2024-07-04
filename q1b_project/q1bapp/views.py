from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.shortcuts import render
from django.http import JsonResponse
from .models import Eventappointment
from .forms import EventForm
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncDay
# login

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print("email",username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Assuming 'home' is the name of your homepage URL pattern
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'Login'})

# logout code - <a class="dropdown-item" href="{% url 'logout' %}"><i class="fa fa-power-off"></i> Logout</a>


def Dashboard(request):
    today = datetime.date.today()
    total_pat = Patient.objects.filter(is_active=True).count()
    open_app = Eventappointment.objects.filter(is_active=True).count()
    close_app = Eventappointment.objects.filter(is_active=False).count()
    today_appointments = Eventappointment.objects.filter(start_time__lte=today,end_time__gte=today).count()

    context = {'total_pat':total_pat,'open_app' : open_app,'close_app':close_app,'today_appointments':today_appointments}
    return render(request,'dashboard.html',context)

import datetime

def Appointments(request):
    patient = Patient.objects.all()
    total_appointments = Eventappointment.objects.all().count()
    today = datetime.date.today()
    # today_appointments = Eventappointment.objects.filter(start_time=today).count()
    today_appointments = Eventappointment.objects.filter(start_time__lte=today,end_time__gte=today).count()

    return render(request,'appointments.html',{'patient':patient,'total_appointments':total_appointments,'today':today,'today_appointments':today_appointments})

def Patientdashboard(request):
    patient = Patient.objects.all()
    return render(request,'patientlist.html',{'patient':patient})

def Appointmentlist(request):
    appointment = Eventappointment.objects.all()
    print("---",appointment)
    return render(request, 'appointmentlist.html', {'appointment': appointment})

def Doctorappointment(request):
    today = datetime.date.today()
    appointment = Eventappointment.objects.filter(
    Q(end_time__gte=today) | Q(start_time=today),
    start_time__lte=today
).first()
    patient = Patient.objects.get(id=appointment.patient_id_id)
    patient_values = Patient.objects.filter(created_at__lte = today)
    return render(request,'doctorappointment.html',{'patient':patient,'patient_values':patient_values})


def patient_data(request):
    print("innnnnnnnnnnnnnnnnnn")
    data = Patient.objects.values('gender').annotate(count=Count('gender')).order_by('gender')
    chart_data = {
        'labels': [item['gender'] for item in data],
        'datasets': [{
            'label': 'Number of Patients by Gender',
            'data': [item['count'] for item in data],
            'backgroundColor': ['rgba(75, 192, 192, 0.2)'] * len(data),
            'borderColor': ['rgba(75, 192, 192, 1)'] * len(data),
            'borderWidth': 1,
        }]
    }
    return JsonResponse(chart_data)

# Appointments calander

def get_events(request):
    events = Eventappointment.objects.all()
    data = []
    for event in events:
        print("==",event.notes)
        data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': event.description,
            'treatment': event.treatment,
            'notes': event.notes,
            'patient': event.patient_id.id,
        })
    return JsonResponse(data, safe=False)
    

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        print("---------",form.errors)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

from django.shortcuts import get_list_or_404, get_object_or_404
def delete_event(request, event_id):
    print("delete")
    if request.method == 'DELETE':
        event = get_object_or_404(Eventappointment, pk=event_id)
        event.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


from django.views.decorators.http import require_http_methods
@require_http_methods(["POST"])
def update_event(request, event_id):
    event = get_object_or_404(Eventappointment, pk=event_id)
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
    


def SubmitPatientForm(request):

    if request.method == 'POST':
        user = request.user  # Get the logged-in user instance
        form = PatientForm(request.POST, request.FILES)  # Include request.FILES for handling file uploads
        print("for-----------m",form.errors)
        if form.is_valid():
            print("sssave")
            form.save()
            return JsonResponse({'message': 'Form submitted successfully'})
        else:
            errors = dict(form.errors.items())  # Convert errors to dictionary
            return JsonResponse({'errors': errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def fetch_patient_data(request):
    patient_id = request.GET.get('patient_id')
    patient = get_object_or_404(Patient, pk=patient_id)
    # Prepare data to send back as JSON
    data = {
        'id': patient.id,
        'registration_id': patient.registration_id,
        'firstname_patient_name': patient.firstname_patient_name,
        'secondname_patient_name': patient.secondname_patient_name,
        'rec_no': patient.rec_no,
        'title': patient.title,
        'mob_no': patient.mob_no,
        'email': patient.email,
        'state': patient.state,
        'city': patient.city,
        'locality': patient.locality,
        'address': patient.address,
        'dob': patient.dob,
        'age': patient.age,
        'second_phone_number': patient.second_phone_number,
        'guardian_name': patient.guardian_name,
        'op_number': patient.op_number,
        'passport_number': patient.passport_number,
        'discharge_date': patient.discharge_date.strftime('%Y-%m-%d') if patient.discharge_date else None,
        'gender': patient.gender,
        'country': patient.country,
        'Medicalhistory': patient.Medicalhistory,
        'zip': patient.zip,
        'bloodgroup': patient.bloodgroup,
        'remarks': patient.remarks,
        'fee': patient.fee,
        'payment': patient.payment,
        'conditions': patient.conditions,
        'pregnant': patient.pregnant,
        'occupation': patient.occupation,
        'specialization': patient.specialization,
        'doctor': patient.doctor,
        'referredBy': patient.referredBy,
        'patient_group': patient.patient_group,
        'register_method': patient.register_method,
        # Add more fields as needed based on your Patient model
    }
    return JsonResponse(data)


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Patient information updated successfully.'})
        else:
            # Return form errors in JSON format
            errors = form.errors.as_json()
            return JsonResponse(errors, status=400)
    
    # If not a POST request, render the form initially
    form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})


def patient_count_per_day(request):
    data = Patient.objects.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    chart_data = {
        'labels': [item['day'].strftime('%Y-%m-%d') for item in data],
        'datasets': [{
            'label': 'Number of Patients per Day',
            'data': [item['count'] for item in data],
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1,
        }]
    }
    return JsonResponse(chart_data)


def get_patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    print("patient",patient)
    patient_data = {
        'registration_id': patient.registration_id,
        'title': patient.title,
        'first_name': patient.firstname_patient_name,
        'last_name': patient.secondname_patient_name,
        'rec_no': patient.rec_no,
        'address': patient.address,
        'locality': patient.locality,
        'city': patient.city,
        'state': patient.state,
        'age': patient.age,
        'mobile_number': patient.mob_no,
        'email': patient.email,
        'dob': patient.dob,
        'gender': patient.gender,
        'guardian_name': patient.guardian_name,
        'op_number': patient.op_number,
        'passport_number': patient.passport_number,
        'discharge_date': patient.discharge_date.strftime('%Y-%m-%d %H:%M:%S') if patient.discharge_date else None,
        'second_phone_number': patient.second_phone_number,
        'country': patient.country,
        'zip_code': patient.zip,
        'blood_group': patient.bloodgroup,
        'medical_history': patient.Medicalhistory,
        'remarks': patient.remarks,
        'fee': patient.fee,
        'payment_status': patient.payment,
        'conditions': patient.conditions,
        'pregnant': patient.pregnant,
        'referred_by': patient.referredBy,
        'occupation': patient.occupation,
        'photo': patient.photo.url if patient.photo else None,
        'specialization': patient.specialization,
        'doctor': patient.doctor,
    }
    return JsonResponse({'patient': patient_data})