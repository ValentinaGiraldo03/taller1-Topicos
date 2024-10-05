from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import EmployeeRegistrationForm, CompanyRegistrationForm, LoginForm, VacancyForm, CommentForm, ApplicationForm, VacancyRatingForm
from .models import Vacancy, Employee, Company, Application
from .services import UserService, VacancyService
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from django.db.models import Avg
from .forms import EmployeeEditForm, CompanyEditForm

'''La razón principal al usar el patrón Singleton 
en UserService es que las operaciones que realiza 
esta clase, como el registro de usuarios, deberían 
ser consistentes y reutilizables en toda la aplicación. 
No tendría sentido crear múltiples instancias de 
esta clase que puedan tener comportamientos 
inconsistentes o fragmentados. El Singleton garantiza 
que la lógica de registro y manejo de usuarios sea 
centralizada y que no haya instancias múltiples 
compitiendo entre sí.'''


def homepage(request):
    return render(request, 'TalentSwapApp/home.html')

def register(request):
    if request.method == 'POST':
        user_type_form = UserTypeForm(request.POST)
        if user_type_form.is_valid():
            user_type = user_type_form.cleaned_data['user_type']
            if user_type == 'company':
                return redirect('register_company')
            elif user_type == 'employee':
                return redirect('register_employee')
    else:
        user_type_form = UserTypeForm()
    return render(request, 'TalentSwapApp/register.html', {'user_type_form': user_type_form})

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            # Usar la instancia Singleton de UserService
            employee_service = UserService()
            employee, error = employee_service.register_employee(form.cleaned_data)
            if error:
                messages.error(request, error)
                return redirect('register_employee')
            messages.success(request, '¡Empleado registrado correctamente!')
            return redirect('login')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'TalentSwapApp/register_employee.html', {'form': form})

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            # Usar la instancia Singleton de UserService
            company_service = UserService()
            company, error = company_service.register_company(form.cleaned_data)
            if error:
                messages.error(request, error)
                return redirect('register_company')
            messages.success(request, '¡Compañía registrada correctamente!')
            return redirect('login')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'TalentSwapApp/register_company.html', {'form': form})

def vacancy_listemployee(request):
    searchTerm = request.GET.get('buscarVacante')
    vacancy_service = VacancyService()  # Usar la instancia Singleton de VacancyService
    vacancies = vacancy_service.search_vacancies(searchTerm)
    return render(request, 'TalentSwapApp/vacancy_listemployee.html', {
        'vacancies': vacancies,
        'searchTerm': searchTerm
    })

def dashboard_employee(request):
    return render(request, 'TalentSwapApp/dashboard_employee.html')

def dashboard_company(request):
    return render(request, 'TalentSwapApp/dashboard_company.html')

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if Company.objects.filter(id=user.id):
                    return redirect('dashboard_company')
                else:
                    return redirect('dashboard_employee')
    context = {'loginform': form}
    return render(request, 'TalentSwapApp/login.html', context=context)

def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def vacancy_detailemployee(request, id):
    vacancy_service = VacancyService()  # Usar la instancia Singleton de VacancyService
    vacancy = vacancy_service.get_vacancy(id)
    comments = vacancy.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.vacancy = vacancy
            new_comment.save()
    else:
        comment_form = CommentForm()

    current_user = request.user
    new_application = None
    if request.method == 'POST':
        application_form = ApplicationForm(data=request.POST)
        if application_form.is_valid():
            new_application = application_form.save(commit=False)
            new_application.vacancy = vacancy
            new_application.user = current_user
            new_application.save()
    else:
        application_form = ApplicationForm()

    return render(request, 'TalentSwapApp/vacancy_detailsemployee.html', {
        'vacancy': vacancy,
        'new_application': new_application,
        'application_form': application_form,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

@login_required
def vacancy_detailcompany(request, id):
    vacancy_service = VacancyService()  # Usar la instancia Singleton de VacancyService
    vacancy = vacancy_service.get_vacancy(id)
    comments = vacancy.comments.all()
    applications = vacancy.applications.filter(status='pending')
    return render(request, 'TalentSwapApp/vacancy_detailscompany.html', {
        'vacancy': vacancy,
        'comments': comments,
        'applications': applications
    })

@login_required
def applied_to_vacancy(request):
    user = request.user
    applications = Application.objects.filter(user=user)
    return render(request, 'TalentSwapApp/applied_to_vacancy.html', {'applications': applications})

def download_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'vacancies', 'GUÍA DE CONTRATO E INFORMACIÓN PERTINENTE.pdf')

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404("El archivo no existe")

def upload_vacancy(request):
        if request.method == "POST":
            form = VacancyForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('vacancy_listcompany')
        else:
            form = VacancyForm()
        return render(request, 'TalentSwapApp/upload_vacancy.html', {'form': form})

@login_required
def rate_vacancy(request, id):
    if request.method == 'POST':
        form = VacancyRatingForm(request.POST)
        if form.is_valid():
            vacancy = get_object_or_404(Vacancy, id=id)
            rating = form.cleaned_data['rating']
            experience = form.cleaned_data['experience']
            
            # Crear una instancia de VacancyRating con los datos del formulario
            vacancy_rating = form.save(commit=False)
            vacancy_rating.vacancy = vacancy
            vacancy_rating.user = request.user
            vacancy_rating.rating = rating
            vacancy_rating.experience = experience
            vacancy_rating.save()

            # Calculando el rating promedio
            ratings = vacancy.ratings.all()
            avg_rating = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']

            return JsonResponse({'message': 'Rating saved successfully', 'avg_rating': avg_rating})
        else:
            # Si el formulario no es válido, devuelve errores de validación
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        # Si la solicitud no es POST, devuelve un error
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def matched_vacancies(request):
    
    if request.user.is_authenticated :
        user_id = request.user.id
        user = Employee.objects.filter(id=user_id)[0] #obtener el usuario de tipo empleado y no el general
        if hasattr(user, 'interests'):
            matched_vacancies = [] # creo la lista donde van a estar las vacantes del match
            interests = set(user.interests.split()) # Convertir los intereses del usuario en un conjunto de palabras
            for vacancy in Vacancy.objects.all():
                vacancy_description_words = set(vacancy.description.split())  # Convertir la descripción de la vacante en un conjunto de palabras
                    # Verificar si hay alguna intersección entre los intereses del usuario y las palabras en la descripción de la vacante
                if interests.intersection(vacancy_description_words): 
                        matched_vacancies.append(vacancy)
    else:
        return redirect('login')

    
    return render(request, 'TalentSwapApp/matched_vacancies.html', {'matched_vacancies': matched_vacancies})


@login_required
def statistics(request):
    # Obtener todos los empleados ordenados por experiencia laboral en meses
    employees = Employee.objects.order_by('work_experience')

    # Calcular estadísticas adicionales si es necesario
    # Por ejemplo, contar el número de empleados o vacantes
    num_employees = employees.count()
    num_vacancies = Vacancy.objects.count()

    # Puedes añadir cualquier otra estadística que desees mostrar
    context = {
        'employees': employees,
        'num_employees': num_employees,
        'num_vacancies': num_vacancies,
    }
    
    return render(request, 'TalentSwapApp/statistics.html', context)

@login_required
def vacancy_listcompany(request):
    searchTerm = request.GET.get('buscarVacante')
    if searchTerm:
        vacanciesName = Vacancy.objects.filter(title__icontains=searchTerm)
        vacanciesDesc = Vacancy.objects.filter(description__icontains=searchTerm)
        vacancies = vacanciesName.union(vacanciesDesc)
    else:
        vacancies = Vacancy.objects.all()
    return render(request, 'TalentSwapApp/vacancy_listcompany.html', {
        'vacancies': vacancies,
        'searchTerm': searchTerm
    })

@login_required
def confirm_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    if request.method == 'POST':
        # Cambiar el estado de la vacante a "no disponible" (status=False)
        vacancy.status = False
        vacancy.save()
        return redirect('vacancy_listemployee')
    return render(request, 'confirm_vacancy.html', {'vacancy': vacancy}) 

@login_required
def reopen_vacancy_company(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    if request.method == 'POST':
        # Cambiar el estado de la vacante a "disponible" (status=True)
        vacancy.status = True
        vacancy.save()
        return redirect('dashboard_company')
    return render(request, 'reopen_vacancy_company.html', {'vacancy': vacancy}) 

@login_required
def profile_view(request):
    user = request.user
    profile = None
    profile_type = None
    show_form = request.GET.get('edit') == 'true'

    if hasattr(user, 'employee'):
        profile = Employee.objects.get(id=user.id)
        profile_type = 'employee'
        form = EmployeeEditForm(instance=profile)
    elif hasattr(user, 'company'):
        profile = Company.objects.get(id=user.id)
        profile_type = 'company'
        form = CompanyEditForm(instance=profile)
    else:
        form = None

    if request.method == 'POST':
        if profile_type == 'employee':
            form = EmployeeEditForm(request.POST, instance=profile)
        elif profile_type == 'company':
            form = CompanyEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Redirige a la vista de perfil después de la actualización

    context = {
        'profile': profile,
        'profile_type': profile_type,
        'form': form,
        'show_form': show_form
    }
    return render(request, 'TalentSwapApp/profile.html', context)
@login_required

def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = None
    profile_type = None

    if hasattr(user, 'employee'):
        profile = user.employee
        profile_type = 'employee'
    elif hasattr(user, 'company'):
        profile = user.company
        profile_type = 'company'

    context = {
        'profile': profile,
        'profile_type': profile_type,
        'viewing': True  # Flag para indicar que es un perfil de visualización, no edición
    }
    return render(request, 'TalentSwapApp/profile_view.html', context)

def users(request):
    template_name = 'TalentSwapApp/users.html'
    searchTerm = request.GET.get('buscarUsuario')
    if searchTerm:
        companies = Company.objects.filter(company_name__icontains=searchTerm)
        employees = Employee.objects.filter(employee_name__icontains=searchTerm)
    else:
        employees = Employee.objects.all()
        companies = Company.objects.all()
    return render(request, template_name, {'searchTerm': searchTerm,'employees': employees, 'companies': companies})