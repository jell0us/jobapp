from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.db.models import Count, Q
from .models import UserDetail, Job, Application
from .forms import LoginForm, ApplicationForm, JobForm, ApplicantRegistrationForm, EmployerRegistrationForm


class LandingPage(TemplateView):
    template_name = 'landing.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', 'applicant')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password or username')
            return redirect('login_user')
        
        if role == 'employer' and not user.is_staff:
            messages.error(request, 'This account is not registered as an Employer.')
            return redirect('login_user')
     
        if role == 'applicant' and user.is_staff:
            messages.error(request, 'This account is an Employer account. Please select Employer.')
            return redirect('login_user')

        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        return redirect('dashboard')

@login_required(login_url='login_user')
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_user')
    return redirect('dashboard')


@login_required(login_url='login_user')
def dashboard(request):
    user = request.user
    total_jobs = Job.objects.count()
 
    if user.is_staff:
        all_apps = Application.objects.select_related('job', 'applicant')
        context = {
            'total_jobs': total_jobs,
            'total_applicants': all_apps.count(),
            'pending_count': all_apps.filter(status='pending').count() if hasattr(Application, 'status') else all_apps.count(),
            'accepted_count': all_apps.filter(status='accepted').count() if hasattr(Application, 'status') else 0,
            'recent_applications': all_apps.order_by('-applied_at')[:5],
        }
    else:
        # Applicant dashboard context
        my_apps = Application.objects.filter(applicant=user).select_related('job')
        context = {
            'total_jobs': total_jobs,
            'applied_count': my_apps.count(),
            'pending_count': my_apps.filter(status='pending').count() if hasattr(Application, 'status') else my_apps.count(),
            'accepted_count': my_apps.filter(status='accepted').count() if hasattr(Application, 'status') else 0,
            'rejected_count': my_apps.filter(status='rejected').count() if hasattr(Application, 'status') else 0,
            'my_applications': my_apps.order_by('-applied_at')[:5],
            'recent_jobs': Job.objects.order_by('-posted_date')[:3],
        }
 
    return render(request, 'dashboard.html', context)

def register_applicant(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['lastname'],
                email=form.cleaned_data['email']
            )

            user_detail = form.save(commit=False)
            user_detail.user = user
            user_detail.role = 'applicant'
            user_detail.save()

            messages.success(request, "Registration successful! You can now sign in.")
            return redirect('login_user')
    else:
        form = ApplicantRegistrationForm()
        
    return render(request, 'register_applicant.html', {'form': form})
    
def register_employer(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('register_employer')
    
        if password.strip() != confirmpassword.strip():
            messages.error(request, 'Password does not match')
            return redirect('register_employer')

        new_user = User.objects.create_user(username=username, email=email, password=password, first_name=company_name)

        UserDetail.objects.create(user=new_user, company_name=company_name, address=address, contactno=contactno, role='employer')

        messages.success(request, 'Employer registered successfully')
        return redirect('dashboard')
        
    else:
        form = EmployerRegistrationForm()  
        return render(request, 'register_employer.html', {'form': form})
    
@login_required(login_url='login_user')
def job_list(request):
   jobs = Job.objects.all()
   return render(request, 'job_list.html', {'jobs': jobs})


@login_required(login_url='login_user')
def job_detail(request, job_id):
   job = get_object_or_404(Job, id=job_id)
   return render(request, 'job_detail.html', {'job': job})

@login_required(login_url='login_user')
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.is_staff:
        messages.error(request, 'Employer accounts cannot apply for jobs.')
        return redirect('job_detail', job_id=job_id)
 
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('my_applications')
 
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            
            messages.success(request, 'Successfully applied for the job!')
            return redirect('my_applications')
        else:
            print("Form errors:", form.errors) 
    else:
        form = ApplicationForm()
 
    return render(request, 'apply_job.html', {'form': form, 'job': job})
 
@login_required(login_url='login_user')
def application_success(request):
    return render(request, 'application_success.html')

@login_required(login_url='login_user')
def application_list(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    applications = Application.objects.all().select_related('job', 'applicant').order_by('-applied_at')
    return render(request, 'application_list.html', {'applications': applications})

@login_required(login_url='login_user')
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    context = {
        'applications': applications,
        'pending_count': applications.filter(status='pending').count() if hasattr(Application, 'status') else applications.count(),
        'accepted_count': applications.filter(status='accepted').count() if hasattr(Application, 'status') else 0,
        'rejected_count': applications.filter(status='rejected').count() if hasattr(Application, 'status') else 0,
    }
    return render(request, 'my_applications.html', context)

@login_required(login_url='login_user')
def post_job(request):
    if request.method == 'POST':
        form =JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})