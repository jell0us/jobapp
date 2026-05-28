from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, ClearableFileInput, PasswordInput, DateInput, FileInput
from .models import Application, Job, UserDetail
from django.contrib.auth.models import User 


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
    email = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': '@juandelacruz'}))
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


class EmployerRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hr@company.com'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'employer_tech'}))
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
    
