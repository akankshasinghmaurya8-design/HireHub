from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from django.utils import timezone
from django.core.mail import send_mail
# Create your views here.
def jobseekerdash(req):
    if 'jsid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    jsid=req.session.get('jsid')
    js=Jobseeker.objects.get(email=jsid)
    app=JobApplication.objects.filter(jobseeker=js)
    shortlisted = JobApplication.objects.filter(jobseeker=js, status="shortlisted")
    rejected = JobApplication.objects.filter(jobseeker=js, status="rejected")
    selected = JobApplication.objects.filter(jobseeker=js, status="selected")
    context={
        'jsid':jsid,
        'js':js,
        'app':app,
        'shortlisted':shortlisted,
        'rejected': rejected,
        'selected': selected,
    }
    return render(req,"jobseekerdash.html",context)


def jslogout(req):
    if 'jsid' not in req.session:
        messages.error(req,"Something went wrong")
        return redirect('login')
    del req.session['jsid']
    messages.success(req,'Logged Out Successfully')
    return redirect('login')

def apply_job(req, jobid):
    if 'jsid' not in req.session:
        messages.error(req, 'Login First')
        return redirect('login')
    jsid =req.session.get('jsid')
    js= Jobseeker.objects.get(email=jsid)
    job = Job.objects.get(id=jobid)
    if job.deadline < timezone.now().date():
        messages.error(req,'Deadline has been passed for this job.')
        return redirect('jobs')
    if JobApplication.objects.filter(jobseeker=js, job=job).exists():
        messages.error(req,'You have already applied for this job.')
        return redirect('jobs')
    jobapp =JobApplication.objects.create(jobseeker = js , job =job)
    messages.success(req,'job application submitted successfully.')
    return redirect('jobs')


def jsprofile(req):
    if 'jsid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    jsid=req.session.get('jsid')
    js=Jobseeker.objects.get(email=jsid)
    app=JobApplication.objects.filter(jobseeker=js)
    context={
        'jsid':jsid,
        'js':js,
        'app':app
    }

    return render(req,'jsprofile.html',context)


def jsedit(req):
    if 'jsid' not in req.session:
        messages.error(req, 'Login first')
        return redirect('login')

    jsid = req.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)

    if req.method == "POST":
        action = req.POST.get("action")

        if action == "personal":
            # Personal + Address + Professional Details
            js.first_name = req.POST.get("first_name")
            js.last_name = req.POST.get("last_name")
            js.dob = req.POST.get("dob")
            js.gender = req.POST.get("gender")
            js.contact_no = req.POST.get("contact_no")
            js.email = req.POST.get("email")

            # Address
            js.locality = req.POST.get("locality")
            js.city = req.POST.get("city")
            js.district = req.POST.get("district")
            js.zip_code = req.POST.get("zip_code")
            js.state = req.POST.get("state")
            js.country = req.POST.get("country")

            # Professional Details
            js.expected_salary = req.POST.get("expected_salary") or None
            js.current_salary = req.POST.get("current_salary") or None
            js.notice_period = req.POST.get("notice_period") or None
            js.linkedin_url = req.POST.get("linkedin_url")
            js.github_url = req.POST.get("github_url")
            js.portfolio_url = req.POST.get("portfolio_url")
            js.is_open_to_work = "is_open_to_work" in req.POST

            # Files
            picture = req.FILES.get("picture")
            resume = req.FILES.get("resume")
            cover_letter = req.FILES.get("cover_letter")

            if picture:
                js.picture = picture
            if resume:
                js.resume = resume
            if cover_letter:
                js.cover_letter = cover_letter

            js.save()
            messages.success(req, "Personal and professional details updated.")
            return redirect("jsedit")

        elif action == "education":
            # Education Save
            Education.objects.create(
                jobseeker=js,
                degree_name=req.POST.get("degree_name"),
                specialization=req.POST.get("specialization"),
                institute=req.POST.get("institute"),
                university=req.POST.get("university"),
                start_year=req.POST.get("start_year"),
                end_year=req.POST.get("end_year"),
            )
            messages.success(req, "Education saved successfully.")
            return redirect("jsedit")

        elif action == "experience":
            # Experience Save
            Experience.objects.create(
                jobseeker=js,
                company_name=req.POST.get("company_name"),
                designation=req.POST.get("designation"),
                start_date=req.POST.get("start_date"),
                end_date=req.POST.get("end_date"),
                description=req.POST.get("description"),
            )
            messages.success(req, "Experience saved successfully.")
            return redirect("jsedit")

        elif action == "skills":
            # Skills Update
            skill_required = req.POST.get('skills')  # कॉमा से अलग स्किल्स
            skill_names = [s.strip() for s in skill_required.split(',') if s.strip()]  # साफ-सुथरा स्किल्स लिस्ट

            job_skill = []
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(skill_name__iexact=name, defaults={'skill_name': name})
                job_skill.append(skill)

            js.skills.set(job_skill)
            js.save()

            messages.success(req, "Skills updated successfully.")
            return redirect("jsedit")

    # GET request context
    context = {
        'jsid': jsid,
        'js': js,
        'skills': Skill.objects.all(),  # सभी उपलब्ध स्किल्स
        'educations': js.educations.all(),  # सभी शिक्षा रिकॉर्ड
        'experiences': js.experiences.all(),  # सभी अनुभव रिकॉर्ड
    }

    return render(req, 'jsedit.html', context)
def jsapplication(req):
    if 'jsid' not in req.session:
        messages.error(req,'Login first')
        return redirect('login')
    jsid=req.session.get('jsid')
    js=Jobseeker.objects.get(email=jsid)
    app=JobApplication.objects.filter(jobseeker=js)
    context={
        'jsid':jsid,
        'js':js,
        'app':app
    }
    return render(req,'jsapplication.html',context)


def jspassword(request):

    if 'jsid' not in request.session:
        messages.error(request, 'Login first')
        return redirect('login')

    jsid = request.session.get('jsid')

    context = {
        'jsid': jsid
    }

    if request.method == 'POST':

        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('conpwd')

        try:
            js = LoginInfo.objects.get(username=jsid)

            # 1. Check confirm password
            if newpwd != confirmpwd:
                messages.warning(request, "New password and confirm password do not match")
                return redirect('jspassword')

            # 2. Check old password
            if oldpwd != js.password:
                messages.warning(request, "Incorrect old password")
                return redirect('jspassword')

            # 3. Prevent same password
            if oldpwd == newpwd:
                messages.warning(request, "New password cannot be same as old password")
                return redirect('jspassword')

            # 4. Save new password
            js.password = newpwd
            js.save()

            messages.success(request, "Password changed successfully")
            return redirect('jspassword')

        except LoginInfo.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('login')

    return render(request, 'jspassword.html', context)


