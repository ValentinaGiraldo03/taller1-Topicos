from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import TextInput, PasswordInput

from .models import Vacancy, Comment, Application, VacancyRating, Employee, Company
# Registro de usuario (Modelo u "objeto" formulario)

class UserTypeForm(forms.Form):
    USER_CHOICES = [
        ('company', 'Company'),
        ('employee', 'Employee'),
    ]
    user_type = forms.ChoiceField(
        label='User Type',
        choices=USER_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'w-4 h-4 border-gray-300 focus:ring-2 focus:ring-blue-300 dark:focus:ring-blue-600 dark:focus:bg-blue-600 dark:bg-gray-700 dark:border-gray-600'
        })
    )

class CompanyRegistrationForm(forms.Form):
    username = forms.CharField(label='Username')
    company_name = forms.CharField(label='Company Name')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    company_type = forms.CharField(label='Company Type')
    information = forms.CharField(label='Information')
    

class EmployeeRegistrationForm(forms.Form):
    username = forms.CharField(label='Username')
    employee_name = forms.CharField(label='Name and Lastname')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    information = forms.CharField(label='Academic Information')
    interests = forms.CharField(label='Interests')
    work_experience = forms.IntegerField(label='Work Experience (months)', min_value=0)

# Autenticación de usuario (Modelo u "objeto" formulario)

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy 
        fields = ('title', 'description', 'document')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ('user', 'vacancy', 'status', 'created_on', 'id')

class VacancyRatingForm(forms.ModelForm):
    class Meta:
        model = VacancyRating
        fields = ['rating', 'experience']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '1', 'max': '5'}),
        }
        error_messages = {
            'rating': {
                'min_value': 'The rating must be at least 1 star.',
                'max_value': 'The rating cannot be more than 5 stars.',
            }
        }

class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_name', 'email', 'information', 'interests', 'work_experience']

class CompanyEditForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'email', 'information', 'company_type']