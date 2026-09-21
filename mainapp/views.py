from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def index(req):
    return render(req,'index.html')
def about(req):
    return render(req,'about.html')
def Register(req):
    if req.method=="POST":
        usertype =req.POST.get('usertype')
        first_name =req.POST.get('first_name')
        last_name =req.POST.get('last_name')
        contact_no =req.POST.get('contact_no')
        email =req.POST.get('email')
        pwd =req.POST.get('pwd')
        confirm_pwd =req.POST.get('confirm_pwd')
        try:
            if pwd!=confirm_pwd:
                messages.warning(req,"Confirm Password should be same")
                return redirect('Register')
            elif LoginInfo.objects.filter(username=email).exists():
                messages.warning(req,"This email already Registered")
                return redirect('Register')
            if usertype=='jobseeker':
                log=LoginInfo(usertype=usertype,username=email,password=pwd)
                js=Jobseeker(user=log,first_name=first_name,last_name=last_name,contact_no=contact_no,email=email)
                log.save()
                js.save()
                messages.success(req,"Registeredv Successfully")
                send_mail(
                        subject="Welcome to HireHub",
                        message=f"""
                        Hello {first_name},

                        Welcome to HireHub!

                        Your account has been successfully created.

                        Thank you for registering with us.

                        Regards,
                        HireHub Team
                        """,
                        from_email="akankshasinghmaurya8@gmail.com",
                        recipient_list=[email],
                        fail_silently=True,
                    )
                return redirect('Register')
            elif usertype=='employer':
                log=LoginInfo(usertype=usertype,username=email,password=pwd)
                emp=Employer(user=log,first_name=first_name,last_name=last_name,contact_no=contact_no,email=email)
                log.save()
                emp.save()
                messages.success(req,"Registered Successfully")
                return redirect('Register')
            
        except Exception as e:
            messages.error(req,f"Something went wrong - {e}")
    return render(req, 'Register.html')
def contact(req):
    if req.method=='POST':
        name=req.POST.get("name")
        email=req.POST.get("email")
        contactno=req.POST.get("contactno")
        subject=req.POST.get("subject")
        message=req.POST.get("message")
        enq=Enquiry(name=name,email=email,contactno=contactno,message=message,subject=subject)
        enq.save()
        messages.success(req,"Enquiry has been successfully sent")
        return redirect('contact')
    return render(req, 'contact.html')
def login(req):
    if req.method=="POST":
        username=req.POST.get('username')
        password=req.POST.get('password')
        try:
            log = LoginInfo.objects.get(username=username,password=password)

            if log is not None:
                if log.usertype == 'admin':
                    req.session['adminid']= log.username
                    messages.success(req,"Welcome admin")
                    return redirect("admindash")
                elif log.usertype == 'jobseeker':
                    
                    req.session['jsid']= log.username
                    messages.success(req, "Welcome Jobseeker")
                    return redirect('jobseekerdash')
                elif log.usertype == 'employer':
                    
                    req.session['empid']= log.username
                    
                    messages.success(req, "Welcome Employer")
                    return redirect('employerdash')

        except LoginInfo.DoesNotExist:
            messages.error(req,"invalid username or password")   
            return redirect('login')   
    return render(req, 'login.html')


def jobs(req):
    job=Job.objects.all().order_by('created_at')
    company=Company.objects.all()
    context ={
        'jobs':job,
        'company':company
    }
    return render(req,'jobs.html',context)