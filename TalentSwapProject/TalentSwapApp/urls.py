from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from .views import download_file

urlpatterns = [

    path('', views.homepage, name='home'),

    path('register/', views.register, name='register'),

    path('register_company/', views.register_company, name='register_company'),

    path('register_employee/', views.register_employee, name='register_employee'),

    path('login/', views.login, name='login'),

    path('dashboard_employee/', views.dashboard_employee, name='dashboard_employee'),

    path('applied_vacancies/', views.applied_to_vacancy, name='applied_to_vacancy'),

    path('dashboard_company/', views.dashboard_company, name='dashboard_company'),

    path('matched_vacancies/', views.matched_vacancies, name='matched_vacancies'),

    path('statistics/', views.statistics, name='statistics'),

    path('logout/', views.logout, name='logout'),

    path('vacanciescompany/' , views.vacancy_listcompany, name= 'vacancy_listcompany'),

    path('vacanciesemployee/' , views.vacancy_listemployee, name= 'vacancy_listemployee'),

    path('confirm_vacancy/<int:vacancy_id>/', views.confirm_vacancy, name='confirm_vacancy'),

    path('reopen_vacancy/<int:vacancy_id>/', views.reopen_vacancy_company, name='reopen_vacancy'),
    
    path('vacancies/upload/' , views.upload_vacancy, name = 'upload_vacancy'),

    path('vacancies/<int:id>/detailemployee/', views.vacancy_detailemployee, name='vacancy_detailemployee'),

    path('vacancies/<int:vacancy_id>/detailcompany/', views.vacancy_detailcompany, name='vacancy_detailcompany'),

    path('vacancy/<int:id>/rate/', views.rate_vacancy, name='rate_vacancy'),

    path('download/', download_file, name='download_file'),

    path('profile/', views.profile_view, name='profile'),
    
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),

    path('users/', views.users, name='usersPage'),

]

#uso de archivos de multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)