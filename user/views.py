from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, Evaluation, TrainingApplications, UserTraining
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm, CustomPasswordResetForm, EvaluationForm, TrainingApplicationForm
from django.db.models import Sum, Avg
import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from datetime import date
from django.utils import timezone


def index(request):
    user = request.user
    courses = TrainingApplications.objects.filter(end_date__lte=date.today(), employee_name=user).count()

    return render(request, "user/index.html", {'courses':courses})

@login_required
@user_passes_test(lambda user: user.is_staff)
def employee_list(request):
    profiles = CustomUser.objects.filter(is_active=True)
    active_users_count = CustomUser.objects.filter(is_active=True).count()
    inactive_profiles = CustomUser.objects.filter(is_active=False)
    inactive_profile_count = inactive_profiles.count()
    return render(request, "user/employee_list.html", {"profiles":profiles, "active_users_count":active_users_count, "inactive_profiles":inactive_profiles, "inactive_profile_count":inactive_profile_count})

@login_required
@user_passes_test(lambda user: user.is_staff)
def inactive_employees(request):
    inactive_profiles = CustomUser.objects.filter(is_active=False)
    print(inactive_profiles)
    inactive_profile_count = inactive_profiles.count()
    return render(request, "user/inactive_employees.html", {"inactive_profiles":inactive_profiles, "inactive_profile_count":inactive_profile_count})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('user:user_list')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('user:index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('user:login')


def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password1']

            try:
                user = CustomUser.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Invalid username')

            return redirect('user:login')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'user/password_reset.html', {'form': form})


# def search(request):
    

#     return render(request, 'user/search_employee.html')


def search_employee(request):
    employees = CustomUser.objects.all()
    search_query = request.GET.get('search_query')

    if search_query:
        employees = employees.filter(first_name__icontains=search_query)  # Apply the training course filter

    context = {'employees': employees, 'search_query':search_query}
    return render(request, 'user/search_employee.html', context)


# def create_evaluation(request):
#     evaluations = Evaluation.objects.all()
#     if request.method == 'POST':
#         form = EvaluationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Handle successful form submission
#     else:
#         form = EvaluationForm()
    
#     context = {'form': form, 'evaluations':evaluations}
#     return render(request, 'user/create_evaluation.html', context)


# def create_evaluation(request):
    

#     if request.method == 'POST':
#         form = EvaluationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Handle successful form submission
#     else:
#         # Filter the available courses based on completed courses
#         print('create_evaluation view')
        
    
#     context = {'form': form}
#     return render(request, 'user/create_evaluation.html', context)


# def evaluation_list(request):
#     evaluations = Evaluation.objects.all()
#     eval_total = evaluations.count()
#     return render(request, 'user/evaluation_list.html', {"evaluations":evaluations, "eval_total":eval_total})


# def evaluation_detail(request, id):
#     evaluation = get_object_or_404(Evaluation, id=id)
#     # Other logic
#     return render(request, 'user/evaluation_detail.html', {"evaluation":evaluation})


def generate_report(request, employee_id):
    # Retrieve Training data for the employee
    training_data = TrainingApplications.objects.filter(employee_id=employee_id)

    # Calculate the total cost for all training courses
    total_cost = training_data.aggregate(Sum('total_cost'))['total_cost__sum']

    # Calculate the total duration in days for all training courses
    total_duration = training_data.aggregate(Sum('no_of_days'))['no_of_days__sum']

    # Define the full and half-day rates as multiplier values
    full_day_rate = 1.0  # Adjust the value as needed
    half_day_rate = 0.5  # Adjust the value as needed

    # Perform calculations only if total_cost is not None
    if total_cost is not None:
        # Calculate the total cost based on the full and half-day rates
        total_cost *= full_day_rate

    # Perform calculations only if total_duration is not None
    if total_duration is not None:
        # Calculate the total duration in hours based on the full and half-day rates
        total_duration *= full_day_rate * 24  # Assuming 1 day = 24 hours

    context = {
        'employee_id': employee_id,
        'training_data': training_data,
        'total_cost': total_cost,
        'total_duration': total_duration,
        # Add other calculated or additional data to the context
    }

    return render(request, 'user/report.html', context)


import csv
from django.http import HttpResponse

def download_csv(request, employee_id):
    # Retrieve Training data for the employee
    training_data = TrainingApplications.objects.filter(employee_id=employee_id)

    # Calculate the total cost for all training courses
    total_cost = training_data.aggregate(Sum('total_cost'))['total_cost__sum']

    # Calculate the total duration in days for all training courses
    total_duration = training_data.aggregate(Sum('no_of_days'))['no_of_days__sum']

    # Define the full and half-day rates as multiplier values
    full_day_rate = 1.0  # Adjust the value as needed
    half_day_rate = 0.5  # Adjust the value as needed

    # Perform calculations only if total_cost is not None
    if total_cost is not None:
        # Calculate the total cost based on the full and half-day rates
        total_cost *= full_day_rate

    # Perform calculations only if total_duration is not None
    if total_duration is not None:
        # Calculate the total duration in hours based on the full and half-day rates
        total_duration *= full_day_rate * 24  # Assuming 1 day = 24 hours

    # Prepare CSV data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Total Cost', 'Total Duration'])

    # Write the employee data to CSV
    writer.writerow([employee_id, total_cost, total_duration])

    return response

def course_application(request):
    '''
    View to render course application form.
    Some fields are prefilled from the users model.
    Redirects to the list view.
    '''
    if request.method == 'POST':
        form = TrainingApplicationForm(request.POST, request=request)
        if form.is_valid():
            application = form.save()
            user_training = UserTraining(user=request.user, training=application)
            user_training.save()
            return redirect('user:course_application_list')
    else:
        form = TrainingApplicationForm(request=request)

    context = {'form': form}
    return render(request, 'user/course_application.html', context)

def course_application_list(request):
    '''
    View to render all courses that an employee has appied for.
    Applications are specifically viewable by logged in user/creator.
    '''
    applications = UserTraining.objects.filter(user=request.user).select_related('training')
    context = {'applications': applications}
    return render(request, 'user/course_application_list.html', context)

def employee_course_application_list(request):
    '''
    View to render all courses that every employee has appied for.
    Applications are only viewable by Admins.
    '''  
    applications = TrainingApplications.objects.all()
    context = {'applications': applications}
    return render(request, 'user/employee_course_application_list.html', context)

def application_detail(request, application_id):
    '''
    View to render detail page for course employee has applied for.
    Details are only viewable by user and they can see application status.
    '''  
    user_training = get_object_or_404(UserTraining, training_id=application_id, user=request.user)
    application = user_training.training
    context = {'application': application}
    return render(request, 'user/course_application_detail.html', context)

def employee_application_detail(request, application_id):
    '''
    View to render detail page for course all employees have applied for.
    Details are only viewable by Admin and includes buttons to approve/deny app.
    ''' 
    application = get_object_or_404(TrainingApplications, id=application_id)
    context = {'application': application}
    return render(request, 'user/employee_course_application_detail.html', context)

def approve_application(request, application_id):
    '''
    Function to allow Admin to approve an employee course application.
    ''' 
    application = get_object_or_404(TrainingApplications, id=application_id)
    application.application_status = 'approved'
    application.save()
    return redirect('user:employee_application_detail', application_id=application.id)

def deny_application(request, application_id):
    '''
    Function to allow Admin to deny an employee course application.
    ''' 
    application = get_object_or_404(TrainingApplications, id=application_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        application.application_status = 'denied'
        application.reason_for_denial = reason
        application.save()
    
    return redirect('user:employee_application_detail', application_id=application.id)

def edit_application(request, application_id):
    '''
    View to edit a course application made by the user.
    '''
    user_training = get_object_or_404(UserTraining, training_id=application_id, user=request.user)
    application = user_training.training

    form = TrainingApplicationForm(request.POST or None, instance=application)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user:application_detail', application_id=application.id)

    context = {'application': application, 'form': form}
    return render(request, 'user/edit_application.html', context)

def delete_application(request, application_id):
    '''
    View to delete a course application made by the user.
    '''
    user_training = get_object_or_404(UserTraining, training_id=application_id, user=request.user)
    application = user_training.training

    if request.method == 'POST':
        # Delete the application
        application.delete()
        return redirect('user:course_application_list')

    context = {'application': application}
    return render(request, 'user/delete_application.html', context)


# Evaluation functionality

def evaluation_list(request):
    # Retrieve evaluations for the logged-in user
    user = request.user
    courses = TrainingApplications.objects.filter(end_date__lte=date.today(), employee_name=user)
    return render(request, 'user/evaluation_list.html', {'courses': courses})

def evaluation_form(request, pk):
    course = get_object_or_404(TrainingApplications, pk=pk)

    # Check if the user has permission to access the evaluation form
    if not request.user.is_superuser and not course.usertraining_set.filter(user=request.user).exists():
        return HttpResponseForbidden("You do not have permission to access this evaluation form.")

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.training_course = course
            evaluation.save()
            return redirect('user:evaluation_list')
    else:
        form = EvaluationForm()
    return render(request, 'user/evaluation_form.html', {'form': form, 'course': course})
