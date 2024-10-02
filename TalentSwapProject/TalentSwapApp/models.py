from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    information = models.TextField()

class Employee(User):
    # Agrega el campo related_name para evitar conflictos con los grupos y permisos de usuario
    groupsemployee = models.ManyToManyField(
        'auth.Group',
        related_name='employee_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    employee_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    work_experience = models.IntegerField(default=0, verbose_name='Experiencia laboral en meses')
    interests = models.TextField()
    employee_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return self.employee_name 

class Company(User):
    # Agrega el campo related_name para evitar conflictos con los grupos y permisos de usuario
    groupscompany = models.ManyToManyField(
        'auth.Group',
        related_name='company_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    company_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='company_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_type = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name

class Vacancy(models.Model):
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='vacancies/', null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author)
    
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_to', null=True, blank=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    information = models.TextField(null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Application for {} by {}'.format(self.vacancy, self.user)
    
class EmployeeRating(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Rating for {self.employee.employee_name}: {self.rating} stars"
    
class VacancyRating(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    experience = models.CharField(max_length=300, default = " No comments")

    def __str__(self):
        return f"Rating {self.rating} for Vacancy {self.vacancy.title} by User {self.user.username}" 
