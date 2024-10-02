from django.contrib import admin
from django.urls import path, include
from TalentSwapApp import views as AppViews



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('TalentSwapApp.urls')),
]
