from django.urls import path
from . import views

urlpatterns=[
    path('employerdash/' ,views.employerdash , name='employerdash'),
    path('emplogout/' , views.emplogout ,name='emplogout'),
    path('empdit/' , views.empedit ,name='empedit'),
    path('empprofile/' , views.empprofile ,name='empprofile'),
    path('postjob/' , views.postjob ,name='postjob'),
    path('postedjob/' , views.postedjob ,name='postedjob'),
    path('save_company/',views.save_company,name='save_company'),
    path('Viewapplicants/<jobid>',views.Viewapplicants,name='Viewapplicants'),
    path('change_status/<appid>',views.change_status,name='change_status'),
    path('deljob/<jobid>',views.deljob,name='deljob'),
     path('emppassword/' , views.emppassword ,name='emppassword'),



]