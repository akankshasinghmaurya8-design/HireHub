from django.shortcuts import render ,redirect
from django.contrib import messages
from mainapp.models import*

# Create your views here.
def admindash(req):
    if 'adminid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    adminid=req.session.get('adminid')
    job_count =Job.objects.all().count()
    js_count=Jobseeker.objects.all().count()
    selected_count = JobApplication.objects.filter(status = 'selected').count
    company_count=Company.objects.all().count()
    context={
        'adminid':adminid,
        'job_count':job_count,
        'js_count':js_count,
        'selected_count':selected_count,
        'company_count':company_count
    }
    return render(req, 'admindash.html',context)

def adminlogout(req):
    if 'adminid' not in req.session:
        messages.error(req,"Something went wrong")
        return redirect('login')
    del req.session['adminid']
    messages.success(req,'Logged Out Successfully')
    return redirect('login')

def addcat(req):
    if 'adminid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    adminid=req.session.get('adminid')
    jobcat=JobCategory.objects.filter()
    context ={
       'adminid':adminid,
       'jobcat':jobcat
   }
    if req.method=="POST":
        category_name=req.POST.get('category_name')
        jobcat=JobCategory(category_name=category_name)
        jobcat.save()
        messages.success(req,"Catagory Added Successfully")
        return redirect('addcat')
    return render(req, 'addcat.html',context)

def employer(req):
    if 'adminid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    adminid =req.session.get('adminid')
    emp=Employer.objects.all()
    context ={
        'adminid':adminid,
        'emp':emp
    }
    return render(req, 'employer.html',context)

def enquires(req):
    if 'adminid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    adminid =req.session.get('adminid')
    enq=Enquiry.objects.all()
    
    context ={
        'adminid':adminid,
        'Enquires':enq
    }
    return render(req, 'enquires.html',context)

def delenq(request , enqid):
    enq = Enquiry.objects.get(id=enqid)
    enq.delete()
    messages.success(request,"Enquiry delete successfully")
    return redirect('enquires')

    

def jobseekers(req):
    if 'adminid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    adminid =req.session.get('adminid')
    
    js= Jobseeker.objects.all()
    context ={
        'adminid':adminid,
        'js':js
    }
    

    return render(req, 'jobseekers.html',context)

def viewcat(req):
    if 'adminid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    adminid =req.session.get('adminid')
    categories=JobCategory.objects.filter()
    context ={
        'adminid':adminid,
        'categories':categories
    }

    return render(req, 'viewcat.html',context)


def delcat(req, id):
    categories=JobCategory.objects.get(id=id)
    categories.delete()
    messages.success(req,"Job Catgory Deleted Sucessfully")
    return redirect('viewcat')
   

def adminpassword(req):
    if 'adminid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    adminid=req.session.get('adminid')
    context={
        'adminid':adminid
    }
    if req.method=='POST':
        oldpwd=req.POST.get('oldpwd')
        newpwd=req.POST.get('newpwd')
        confirmpwd=req.POST.get('conpwd')
        try:
            admin=LoginInfo.objects.get(username=adminid)
            if newpwd!=confirmpwd:
                messages.warning(req,"New Password Should be shame as Confirm Password")
                return redirect('adminpassword')
            elif oldpwd!=admin.password:
                messages.warning(req,"Incorrect password")
                return redirect('adminpassword')
            elif oldpwd==newpwd:
                messages.warning(req,"Password can't be repeated")
                return redirect('adminpassword')
            admin.password=newpwd
            admin.save()
            messages.success(req,"Password Change Successfully")
            return redirect('adminpassword')
        except:LoginInfo.DoesNotExist
        messages.warning(req,"Something Went Wrong")

    return render(req, 'adminpassword.html',context)
