"""
URL configuration for django_job project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from job_app import views
from job_app.views import LandingPage


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', LandingPage.as_view(), name='landing_view'),
   path('login/', views.login_user, name='login_user'),
   path('logout/', views.logout_user, name='logout_user'),
   path('register/', views.register_applicant, name='register_applicant'),
   path('register/employer/', views.register_employer, name='register_employer'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('jobs/', views.job_list, name='job_list'),
   path('job/<int:job_id>/', views.job_detail, name='job_detail'),
   path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
   path('job/post/', views.post_job, name='post_job'),
   path('application/success/', views.application_success, name='application_success'),
   path('applications/', views.application_list, name='application_list'),
   path('my_applications/', views.my_applications, name='my_applications'),
   path('applications/<int:application_id>/status/<str:status>/', views.update_application_status, name='update_status'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)