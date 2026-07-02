from django.urls import path
from . import views
urlpatterns=[
    path('admindash/' , views.admindash, name='admindash'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('addcat/' , views.addcat, name='addcat'),
    path('viewcat/' , views.viewcat, name='viewcat'),
    path('employer/' , views.employer, name='employer'),
    path('jobseekers/' , views.jobseekers, name='jobseekers'),
    path('enquires/' , views.enquires, name='enquires'),
     path('adminpassword/' , views.adminpassword, name='adminpassword'),
     path('delenq/<enqid>',views.delenq,name='delenq'),
      path('delcat/<id>',views.delcat,name='delcat'),
    



]