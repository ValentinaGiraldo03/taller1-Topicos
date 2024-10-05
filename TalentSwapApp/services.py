from .models import Employee, Company, Vacancy, Application
from .forms import VacancyForm

class UserService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UserService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_employee(self, data):
        email = data['email']
        if Employee.objects.filter(username=email).exists():
            return None, 'Este correo ya está registrado.'
        
        employee = Employee.objects.create_user(
            username=email,
            email=email,
            password=data['password'],
            information=data['information']
        )
        employee.employee_name = data['employee_name']
        employee.interests = data['interests']
        employee.work_experience = data['work_experience']
        employee.save()
        return employee, None

    def register_company(self, data):
        if Company.objects.filter(username=data['email']).exists():
            return None, 'Este correo ya está registrado.'
        
        company = Company.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            information=data['information']
        )
        company.company_name = data['company_name']
        company.company_type = data['company_type']
        company.save()
        return company, None

class VacancyService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VacancyService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def search_vacancies(self, searchTerm):
        if searchTerm:
            vacanciesName = Vacancy.objects.filter(title__icontains=searchTerm)
            vacanciesDesc = Vacancy.objects.filter(description__icontains=searchTerm)
            return vacanciesName.union(vacanciesDesc)
        return Vacancy.objects.all()

    def get_vacancy(self, id):
        return Vacancy.objects.get(id=id)
    
    def create_vacancy(self, data):
        form = VacancyForm(data)
        if form.is_valid():
            form.save()
            return form
        return None
