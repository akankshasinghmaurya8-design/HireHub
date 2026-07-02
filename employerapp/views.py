from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *

# Create your views here.
def employerdash(req):
    if 'empid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    empid = req.session.get('empid')

    emp = Employer.objects.get(email=empid)

    jobs = Job.objects.filter(employer=emp)

    total_jobs = jobs.count()

    active_jobs = jobs.filter(is_active=True).count()

    applications = JobApplication.objects.filter(job__employer=emp)

    total_applications = applications.count()

    shortlisted = applications.filter(status='shortlisted').count()

    recent_jobs = jobs.order_by('-created_at')[:5]

    recent_applications = applications.order_by('-applied_at')[:5]

    context = {
        'emp': emp,
        'jobs': jobs,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
    }
    return render(req,'employerdash.html',context)


def emplogout(req):
    if 'empid' not in req.session:
        messages.error(req,"Something went wrong")
        return redirect('login')
    del req.session['empid']
    messages.success(req,'Logged Out Successfully')
    return redirect('login')

def empedit(req):
    if 'empid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    empid=req.session.get('empid')
    emp=Employer.objects.get(email=empid)
    context={
        'empid':empid,
        'emp':emp
    }
    if req.method=="POST":
        first_name =req.POST.get('first_name')
        last_name=req.POST.get('last_name')
        dob=req.POST.get('dob')
        gender=req.POST.get('gender')
        contact_no=req.POST.get('contact_no')
        designation=req.POST.get('designation')
        picture=req.FILES.get('picture')
        #update code
        emp.first_name=first_name
        emp.last_name=last_name
        emp.dob=dob
        emp.gender=gender
        emp.contact_no=contact_no
        emp.designation=designation
        if picture:
            emp.picture=picture
        emp.save()
        messages.success(req,'Personal details updated')
        return redirect('empedit')
    
    return render(req,'empedit.html',context)

def empprofile(req):
    if 'empid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    empid=req.session.get('empid')
    emp=Employer.objects.get(email=empid)
    context={
        'empid':empid,
        'emp':emp
    }
    return render(req,'empprofile.html',context)


def postedjob(req):
    if 'empid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    empid=req.session.get('empid')
    emp=Employer.objects.get(email=empid)
    jobs=Job.objects.filter(employer=emp,company=emp.company)
    context={
        'empid':empid,
        'emp':emp,
        'jobs':jobs
    }
    return render(req,'postedjob.html',context)
def postjob(req):
    if 'empid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    empid=req.session.get('empid')
    emp=Employer.objects.get(email=empid)
    categories=JobCategory.objects.all()
    context={
        'empid':empid,
        'emp':emp,
        'categories':categories
    }
    if req.method =="POST":
        cat=None
        catid=req.POST.get('catid')
        if catid:
            cat = JobCategory.objects.get(id=catid)
        
        title = req.POST.get('title')
        description = req.POST.get('description')
        job_type = req.POST.get('job_type')
        salary = req.POST.get('salary')
        location=req.POST.get('location')
        skill_required = req.POST.get('skill_required')
        vacancy = req.POST.get('vacancy')
        deadline = req.POST.get('deadline')
        job=Job.objects.create(category=cat,employer=emp,company=emp.company,
             title=title,description=description,job_type=job_type,salary=salary,
             location=location,vacancy=vacancy,deadline=deadline)
        if skill_required:
            job_skill =[]
            skill_names=[s.strip() for s in skill_required.split(',') if s.strip()]
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(skill_name__iexact = name,defaults={'skill_name':name})
                job_skill.append(skill)
            job.skills_required.set(job_skill) 
        job.save() 
        messages.success(req,"Job posted successfully")
        return redirect('postjob')
    return render(req,'postjob.html',context)


def save_company(req):
    if 'empid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    empid=req.session.get('empid')
    emp=Employer.objects.get(email=empid)
    if req.method == "POST":
        company_name = req.POST.get('company_name')
        contact_no = req.POST.get('contact_no')
        email = req.POST.get('email')
        location = req.POST.get('location')
        logo = req.FILES.get('logo')
        website = req.POST.get('website')
        industry = req.POST.get('industry')
        established_at = req.POST.get('established_at')
        details = req.POST.get('details')
        comp=Company.objects.create(company_name=company_name,
                                    contact_no=contact_no,email=email,location=location,
                                    logo=logo,website=website,industry=industry,established_at=established_at,details=details)
        
        emp.company=comp
        emp.save()
        messages.success(req,'Company detail created')
        return redirect('empedit')

    else:
        return redirect('empedit')
   


def Viewapplicants(req, jobid):
    if 'empid' not in req.session:
        messages.error(req, 'Login first')
        return redirect('login')

    empid = req.session.get('empid')
    emp = Employer.objects.get(email=empid)

    job = Job.objects.get(id=jobid)

    apps = JobApplication.objects.filter(job=job).select_related('jobseeker')

    context = {
        'empid': empid,
        'emp': emp,
        'apps': apps,
    }

    return render(req, 'Viewapplicants.html', context)


def change_status(req ,appid):
    if 'empid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    app=JobApplication.objects.get(id=appid)
    if req.method=="POST":
        status = req.POST.get('status')
        app.status =status
        app.save()
        messages.success(req, "Application status change")
        return redirect('Viewapplicants',jobid=app.job.id)
    else:
        return redirect('Viewapplicants',jobid=app.job.id)
    

def deljob(req,jobid):
    job=Job.objects.get(id=jobid)
    job.delete()
    messages.success(req,"Employee delete successfully")
    return redirect('postedjob')

def emppassword(request):

    if 'empid' not in request.session:
        messages.error(request, 'Login first')
        return redirect('login')

    empid = request.session.get('empid')

    context = {
        'empid': empid
    }

    if request.method == 'POST':

        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('conpwd')

        try:
            emp = LoginInfo.objects.get(username=empid)

            # 1. Check confirm password
            if newpwd != confirmpwd:
                messages.warning(request, "New password and confirm password do not match")
                return redirect('jspassword')

            # 2. Check old password
            if oldpwd != emp.password:
                messages.warning(request, "Incorrect old password")
                return redirect('emppassword')

            # 3. Prevent same password
            if oldpwd == newpwd:
                messages.warning(request, "New password cannot be same as old password")
                return redirect('emppassword')

            # 4. Save new password
            emp.password = newpwd
            emp.save()

            messages.success(request, "Password changed successfully")
            return redirect('jspassword')

        except LoginInfo.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('login')

    return render(request, 'emppassword.html', context)


