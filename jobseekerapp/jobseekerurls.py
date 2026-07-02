from django.urls import path
from.import views
urlpatterns=[
    path('jobseekerdash/',views.jobseekerdash,name='jobseekerdash'),
    path('jslogout/',views.jslogout,name='jslogout'),
    path('jsprofile/', views.jsprofile, name='jsprofile'),
    path('jsedit/', views.jsedit, name='jsedit'),
    path('jsapplication/', views.jsapplication, name='jsapplication'),
    path('apply_job/<jobid>',views.apply_job , name='apply_job'),
    path('jspassword/',views.jspassword,name='jspassword'),

]