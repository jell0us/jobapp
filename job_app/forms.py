from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, PasswordInput, DateInput, FileInput
from .models import Application, Job, UserDetail, Message
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username', 'id': 'username'}),
            'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password', 'id': 'password'}),
        }


class ApplicantRegistrationForm(forms.ModelForm):
    firstname = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan'}))
    lastname = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Dela Cruz'}))
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'juandelacruz'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'juan@dela-cruz.com'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))
    confirmpassword = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))

    class Meta:
        model = UserDetail
        fields = ['birthdate', 'gender', 'address', 'contactno']
        widgets = {
            'birthdate': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-select', 'id': 'gender'}, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')]),
            'address': Textarea(attrs={'class': 'form-control', 'placeholder': 'Laguindingan, Misamis Oriental', 'rows': '3'}),
            'contactno': TextInput(attrs={'class': 'form-control', 'placeholder': '09XX-XXX-XXXX'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address (e.g. user@gmail.com).")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirmpassword")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirmpassword', "Passwords do not match.")
        return cleaned_data


class EmployerRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hr@company.com'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employer Tech.'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))
    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))

    class Meta:
        model = UserDetail
        fields = ['company_name', 'gender', 'address', 'contactno']
        widgets = {
            'company_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name (e.g., Tech Corp)'}),
            'gender': Select(attrs={'class': 'form-select', 'id': 'gender'}, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')]),
            'address': Textarea(attrs={'class': 'form-control', 'placeholder': 'Business Address', 'rows': '3'}),
            'contactno': TextInput(attrs={'class': 'form-control', 'placeholder': '09XX-XXX-XXXX'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address (e.g. hr@company.com).")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirmpassword")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirmpassword', "Passwords do not match.")
        return cleaned_data


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'status']
        widgets = {
            'resume': FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select', 'id': 'status'}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Developer, Marketing Manager'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the role, responsibilities, and what a typical day looks like...'}),
            'requirements': Textarea(attrs={'class': 'form-control', 'placeholder': 'List skills, experience, education, or certifications needed...'}),
        }


# FEATURE 2 — Job Edit Form (same fields as JobForm, reused for editing)
class JobEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'requirements': Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }


# FEATURE 3 — Applicant Profile Edit Form (unchanged)
class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan'})
    )
    last_name = forms.CharField(
        required=False,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Dela Cruz'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'juan@gmail.com'})
    )
    username = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserDetail
        fields = ['birthdate', 'gender', 'address', 'contactno']
        widgets = {
            'birthdate': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-select'}, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')]),
            'address': Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'contactno': TextInput(attrs={'class': 'form-control', 'placeholder': '09XX-XXX-XXXX'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address (e.g. user@gmail.com).")
        return email


# FEATURE 1 — Form for composing a new message (employer → applicant)
class ComposeMessageForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        required=False,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Regarding your application for Software Developer'})
    )
    message_body = forms.CharField(
        widget=Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Write your message here...'})
    )


# FEATURE 1 — Form for replying to a message (applicant → employer)
class ReplyMessageForm(forms.Form):
    message_body = forms.CharField(
        widget=Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Write your reply here...'})
    )
