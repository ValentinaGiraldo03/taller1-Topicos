from .models import Employee, Company, Vacancy, Application
from .forms import VacancyForm

class UserService:
    @staticmethod
    def register_employee(data):
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

    @staticmethod
    def register_company(data):
        company = Company.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            information=data['information']
        )
        company.company_name = data['company_name']
        company.company_type = data['company_type']
        company.save()
        return company

class VacancyService:
    @staticmethod
    def search_vacancies(searchTerm):
        if searchTerm:
            vacanciesName = Vacancy.objects.filter(title__icontains=searchTerm)
            vacanciesDesc = Vacancy.objects.filter(description__icontains=searchTerm)
            return vacanciesName.union(vacanciesDesc)
        return Vacancy.objects.all()

    @staticmethod
    def get_vacancy(id):
        return Vacancy.objects.get(id=id)
    
    @staticmethod
    def create_vacancy(data):
        form = VacancyForm(data)
        if form.is_valid():
            form.save()
            return form
        return None


