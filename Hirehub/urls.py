"""
URL configuration for Hirehub project.

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
from django.urls import path ,include
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('adminapp/',include('adminapp.adminappurls')), # adminapp ki url file ko add karna
    path('jobseekerapp/',include('jobseekerapp.jobseekerurls')),
    path('employerapp/',include('employerapp.employerurls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='home'),
    path('contact/',views.contact , name='contact'),
     path('Register/',views.Register , name='Register'),
     path('jobs/' ,views.jobs , name='jobs'),
     path('login/', views.login , name='login'),
     path('about/', views.about , name='about'),
         
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
