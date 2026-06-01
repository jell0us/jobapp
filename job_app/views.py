from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import UserDetail, Job, Application, Message
from .forms import ( LoginForm, ApplicationForm, JobForm, JobEditForm, ApplicantRegistrationForm, EmployerRegistrationForm,
    EditProfileForm, ComposeMessageForm, ReplyMessageForm,)
from django.http import HttpResponseForbidden


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
        # FEATURE 1 — Unread message count for employer dashboard
        unread_count = Message.objects.filter(receiver=user, is_read=False).count()
        context = {
            'total_jobs': total_jobs,
            'total_applicants': all_apps.count(),
            'pending_count': all_apps.filter(status='pending').count(),
            'accepted_count': all_apps.filter(status='accepted').count(),
            'recent_applications': all_apps.order_by('-applied_at')[:5],
            'unread_count': unread_count,
        }
    else:
        my_apps = Application.objects.filter(applicant=user).select_related('job')
        recent_jobs = Job.objects.order_by('-posted_date')[:3]
        applied_job_ids = my_apps.values_list('job_id', flat=True)
        for job in recent_jobs:
            job.has_applied = job.id in applied_job_ids

        # FEATURE 1 — Unread message count for applicant dashboard
        unread_count = Message.objects.filter(receiver=user, is_read=False).count()

        context = {
            'total_jobs': total_jobs,
            'applied_count': my_apps.count(),
            'pending_count': my_apps.filter(status='pending').count(),
            'accepted_count': my_apps.filter(status='accepted').count(),
            'rejected_count': my_apps.filter(status='rejected').count(),
            'my_applications': my_apps.order_by('-applied_at')[:5],
            'recent_jobs': recent_jobs,
            'unread_count': unread_count,
        }

    return render(request, 'dashboard.html', context)


def register_applicant(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another one.")
                return render(request, 'register_applicant.html', {'form': form})

            user = User.objects.create_user(
                username=username,
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
        form = EmployerRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            company_name = form.cleaned_data['company_name']
            address = form.cleaned_data['address']
            contactno = form.cleaned_data['contactno']

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return render(request, 'register_employer.html', {'form': form})

            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=company_name,
                is_staff=True
            )
            UserDetail.objects.create(
                user=new_user,
                company_name=company_name,
                address=address,
                contactno=contactno,
                role='employer'
            )

            messages.success(request, 'Employer registered successfully')
            return redirect('login_user')

    else:
        form = EmployerRegistrationForm()

    return render(request, 'register_employer.html', {'form': form})


@login_required(login_url='login_user')
def job_list(request):
    jobs = Job.objects.all()

    if not request.user.is_staff:
        applied_job_ids = Application.objects.filter(
            applicant=request.user
        ).values_list('job_id', flat=True)

        for job in jobs:
            job.has_applied = job.id in applied_job_ids

    return render(request, 'job_list.html', {'jobs': jobs})


@login_required(login_url='login_user')
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    has_applied = False
    if request.user.is_authenticated and not request.user.is_staff:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    context = {
        'job': job,
        'has_applied': has_applied
    }
    return render(request, 'job_detail.html', context)


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
            application.status = 'pending'
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
        'pending_count': applications.filter(status='pending').count(),
        'accepted_count': applications.filter(status='accepted').count(),
        'rejected_count': applications.filter(status='rejected').count(),
    }
    return render(request, 'my_applications.html', context)


@login_required(login_url='login_user')
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})


@login_required
def update_application_status(request, application_id, status):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to perform this action.")

    if status in ['accepted', 'rejected', 'pending']:
        application = get_object_or_404(Application, id=application_id)
        application.status = status
        application.save()

    return redirect(request.META.get('HTTP_REFERER', 'application_list'))


# ---------------------------------------------------------------------------
# FEATURE 2 — Edit and Delete Job Listing
# ---------------------------------------------------------------------------

@login_required(login_url='login_user')
def edit_job(request, job_id):
    """Employer edits their own job listing."""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Only the employer who posted this job can edit it
    if job.posted_by != request.user:
        messages.error(request, 'You can only edit your own job listings.')
        return redirect('job_list')

    if request.method == 'POST':
        form = JobEditForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job listing "{job.title}" updated successfully.')
            return redirect('job_list')
    else:
        form = JobEditForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required(login_url='login_user')
def delete_job(request, job_id):
    """Employer deletes their own job listing."""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Only the employer who posted this job can delete it
    if job.posted_by != request.user:
        messages.error(request, 'You can only delete your own job listings.')
        return redirect('job_list')

    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f'Job listing "{job_title}" deleted successfully.')
        return redirect('job_list')

    # GET — show confirmation page
    return render(request, 'delete_job.html', {'job': job})


# ---------------------------------------------------------------------------
# FEATURE 1 — Internal Messaging System
# ---------------------------------------------------------------------------

@login_required(login_url='login_user')
def inbox(request):
    """
    Shows the message inbox for the logged-in user.
    Groups top-level messages (no parent) so threads are not duplicated.
    Newest first.
    """
    # Collect all top-level messages where the user is sender or receiver
    user = request.user
    received = Message.objects.filter(
        receiver=user,
        parent__isnull=True
    ).select_related('sender', 'related_job').order_by('-timestamp')

    sent = Message.objects.filter(
        sender=user,
        parent__isnull=True
    ).select_related('receiver', 'related_job').order_by('-timestamp')

    unread_count = Message.objects.filter(receiver=user, is_read=False).count()

    context = {
        'received': received,
        'sent': sent,
        'unread_count': unread_count,
    }
    return render(request, 'inbox.html', context)


@login_required(login_url='login_user')
def view_thread(request, message_id):
    """
    Shows the full conversation thread starting from a top-level message.
    Marks all messages in the thread as read for the current user.
    Allows replying.
    """
    user = request.user
    # Get the root message of the thread
    root_message = get_object_or_404(Message, id=message_id)

    # Security: only sender or receiver of the root message can view the thread
    if root_message.sender != user and root_message.receiver != user:
        messages.error(request, 'You do not have access to this conversation.')
        return redirect('inbox')

    # Collect all replies for this thread
    thread_replies = Message.objects.filter(
        parent=root_message
    ).select_related('sender', 'receiver').order_by('timestamp')

    # Mark all messages in thread as read if the current user is the receiver
    if root_message.receiver == user and not root_message.is_read:
        root_message.is_read = True
        root_message.save()

    thread_replies.filter(receiver=user, is_read=False).update(is_read=True)

    # Determine the "other party" for the reply form
    if root_message.sender == user:
        other_party = root_message.receiver
    else:
        other_party = root_message.sender

    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                sender=user,
                receiver=other_party,
                related_job=root_message.related_job,
                subject=root_message.subject,
                message_body=form.cleaned_data['message_body'],
                parent=root_message,
                is_read=False,
            )
            messages.success(request, 'Reply sent.')
            return redirect('view_thread', message_id=root_message.id)
    else:
        form = ReplyMessageForm()

    context = {
        'root_message': root_message,
        'thread_replies': thread_replies,
        'form': form,
        'other_party': other_party,
    }
    return render(request, 'view_thread.html', context)


@login_required(login_url='login_user')
def compose_message(request, applicant_id):
    """
    Employer composes a new message to a specific applicant.
    Only employers can access this view.
    """
    if not request.user.is_staff:
        messages.error(request, 'Only employers can send messages.')
        return redirect('dashboard')

    applicant = get_object_or_404(User, id=applicant_id, is_staff=False)

    # Optional: pre-select a related job if ?job_id=X is passed
    job = None
    job_id = request.GET.get('job_id') or request.POST.get('job_id')
    if job_id:
        job = Job.objects.filter(id=job_id).first()

    if request.method == 'POST':
        form = ComposeMessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                sender=request.user,
                receiver=applicant,
                related_job=job,
                subject=form.cleaned_data.get('subject', ''),
                message_body=form.cleaned_data['message_body'],
                is_read=False,
            )
            messages.success(request, f'Message sent to {applicant.get_full_name() or applicant.username}.')
            return redirect('inbox')
    else:
        form = ComposeMessageForm()

    context = {
        'form': form,
        'applicant': applicant,
        'job': job,
    }
    return render(request, 'compose_message.html', context)


# ---------------------------------------------------------------------------
# FEATURE 3 — Applicant Profile Editing (unchanged, kept as-is)
# ---------------------------------------------------------------------------

@login_required(login_url='login_user')
def edit_profile(request):
    if request.user.is_staff:
        messages.error(request, 'Employers cannot use the applicant profile editor.')
        return redirect('dashboard')

    user = request.user
    user_detail = get_object_or_404(UserDetail, user=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user_detail)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            new_username = form.cleaned_data['username']
            if new_username != user.username:
                if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                    messages.error(request, 'That username is already taken.')
                    return render(request, 'edit_profile.html', {'form': form})
                user.username = new_username

            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = EditProfileForm(instance=user_detail, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
        })

    return render(request, 'edit_profile.html', {'form': form})
