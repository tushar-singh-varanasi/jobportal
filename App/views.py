import random
from django.conf import settings
from django.contrib.auth import get_user_model
# from datetime import datetime
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse,HttpResponseRedirect
from .forms import( CustomUsercreationForm,RecruiterForm,AuthenticationCustomForm,CandidateDetailsForm,ApplyForm)
UserModel = get_user_model()
from .models import (MyUser,Candidate,Recruiter,Apply)
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.core.mail import send_mail  
from django.core.exceptions import ValidationError
from django.views.generic.edit import UpdateView
# from django.contrib.auth.decorators import login_required
from .decorators import custom_login_required_hr,custom_login_required_candidate

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q 




def home(request):
    query = request.GET.get('q')
    query1 = request.GET.get('q1')
    
  
    items_list = Recruiter.objects.all().order_by('date')
    #      # Pagination
    if query and query1:
        items_list = items_list.filter(Q(Position__icontains=query) | Q(Categories__icontains=query1))
    elif query:
        items_list = items_list.filter(Q(Position__icontains=query))
    elif query1:
        items_list = items_list.filter(Q(Categories__icontains=query1))
    page = request.GET.get('page')
    paginator = Paginator(items_list, 1)  # Show 1 items per page
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results.
        items = paginator.page(paginator.num_pages)
    return render(request, 'home/index.html', {'items': items})




def Job_filter(request,data=None):
    if data==None:
        form=Recruiter.objects.all()
    elif data == 'marketing':
        form=Recruiter.objects.filter(Categories='marketing')
    elif data == 'Information Tech':
        form=Recruiter.objects.filter(Categories='Information Tech')
    elif data == 'Construction':
        form=Recruiter.objects.filter(Categories='Construction')
    elif data == 'Graphic design':
        form=Recruiter.objects.filter(Categories='Graphic design')

    return render(request,'home/job_catagory.html',{'form':form})

    
def Signupform_cand(request):
    if request.method == 'POST':
        form = CustomUsercreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Generate and store the OTP in the session
            otp = random.randrange(1000, 9999)
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['password'] = password

            # Send OTP to the user's email
            subject = 'Your OTP for Account Verification'
            message = f'Your OTP is: {otp}'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "OTP sent to your email. Please enter it for verification.")
                return redirect('/otp-candidate/')  # Redirect to the OTP verification page
            except Exception as e:
                # If there's an error while sending the email, handle it gracefully
                messages.error(request, "Failed to send OTP email. Please try again later.")
                return render(request, 'home/signup.html', {'form': form})
    else:
        form = CustomUsercreationForm()
    return render(request, 'home/signup.html', {'form': form})

def OTPFunction_can(request):
    if request.session.get('email'):
        if request.method == 'POST':
            otp = request.POST.get('otp')
           
            if int(otp) == request.session.get('otp'):
                useremail = request.session['email']
                userpassword = request.session['password']
                password = make_password(userpassword)
                user = MyUser(email=useremail, password=password)
                user.save()
                recruiter_group,create= Group.objects.get_or_create(name='Candidate')
                recruiter_group.user_set.add(user)
                del request.session['email']
                del request.session['password']
                del request.session['otp']
                messages.success(request, "Account created successfully.")
                # print('User created successfully')
                return redirect('/login-Candidate/')
            else:
                messages.warning(request, "invalid otp")
                return render(request, 'home/otp.html')

            
               
        else:
            return render(request, 'home/otp.html')
    else:
        messages.error(request, "Authentication error. Please sign up again.")
        print("Not authenticated")
        return redirect('/')

################## For REcruter
def Signupform_HR(request):
    if request.method == 'POST':
        form = CustomUsercreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Generate and store the OTP in the session
            otp = random.randrange(1000, 9999)
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['password'] = password

            # Send OTP to the user's email
            subject = 'Your OTP for Account Verification'
            message = f'Your OTP is: {otp}'
            from_email = 'your_email@example.com'  # Replace with your email address
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "OTP sent to your email. Please enter it for verification.")
                return redirect('/otphr/')  # Redirect to the OTP verification page
            except Exception as e:
                # If there's an error while sending the email, handle it gracefully
                messages.error(request, "Failed to send OTP email. Please try again later.")
                return render(request, 'home/signup.html', {'form': form})
    else:
        form = CustomUsercreationForm()
    return render(request, 'home/signup.html', {'form': form})




def OTPFunction_HR(request):
    if request.session.get('email'):
        if request.method == 'POST':
            otp = request.POST.get('otp')
           
            if int(otp) == request.session.get('otp'):
                useremail = request.session['email']
                userpassword = request.session['password']
                password = make_password(userpassword)
                user = MyUser(email=useremail, password=password)
                user.save()
                recruiter_group,create= Group.objects.get_or_create(name='recruiter')
                recruiter_group.user_set.add(user)

                del request.session['email']
                del request.session['password']
                del request.session['otp']

                messages.success(request, "Account created successfully.")
                # print('User created successfully')
                return redirect('/profile-hr/')
            else:
                messages.warning(request, "invalid otp")
                return render(request, 'home/otp.html')

                   
        else:
            return render(request, 'home/otp.html')
    else:
        messages.error(request, "Authentication error. Please sign up again.")
        # print("Not authenticated")
        return redirect('/')


@custom_login_required_hr
def job_post(request):
    if request.method=='POST':
        Company_Name=request.POST['Company_Name']
        Position=request.POST['Position']
        job_description=request.POST['job_description']
        Salary=request.POST['Salary']
        Categories=request.POST['Categories']
        user_obj=Recruiter( Company_Name=Company_Name,Position=Position,job_description=job_description,Salary=Salary,Categories=Categories)
        user_obj.save()
        user_obj.user=request.user
        user_obj.save()
    else:
        pass
    return render(request,'Hr/recruter.html') 

# @custom_login_required_hr
class JOB_Post_update(UpdateView):
    template_name='HR/job_post_update.html'
    model=Recruiter
    form_class=RecruiterForm
    success_url='/profile/'
    

@custom_login_required_hr
def Job_edit(request):
    data=Recruiter.objects.filter(user=request.user)
    return render(request,'HR/job_edit.html',{'data':data})

@custom_login_required_hr
def  Job_delete(request, id):
    data = get_object_or_404(Recruiter, id=id) 
    data.delete()
    return redirect('/job-edit/')

   
def loginfunctionHR(request):
    if request.method=='POST':
        form=AuthenticationCustomForm(request=request, data=request.POST)
        if form.is_valid():
            email=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request,user)
                return redirect('/profile-hr/')
    else:
        form=AuthenticationCustomForm()

    return render(request,'auth/login.html',{'form':form})  

def loginfunction_Candidate(request):
    if request.method=='POST':
        form=AuthenticationCustomForm(request=request, data=request.POST)
        if form.is_valid():
            email=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request,user)
                return redirect('/Profile-Candidate/')
    else:
        form=AuthenticationCustomForm()

    return render(request,'auth/login_Candidate.html',{'form':form})  


def logout_view(request):
   logout(request)
   return redirect('/')

@custom_login_required_hr
def Profile(request):
    if request.user.groups.filter(name='recruiter').exists():
        
        return render(request,'Hr/profile.html')
    else:
        return redirect('/logout/')

@custom_login_required_candidate
def Profile_candidate(request):
    if request.user.groups.filter(name='Candidate').exists():
        candidate_data=Candidate.objects.filter(user=request.user)
        # print('hello',candidate_data.Name)
        return render(request,'Candidate/profile.html',{'candidate_data':candidate_data})
    else:
        return redirect('/logout/')


def Candidate_detail(request):
    if request.user.is_authenticated:

        try:
            # user=request.user
            user_candidate = Candidate.objects.get(user=request.user)
            data=user_candidate.id
            request.session['data'] =data
            # If a Candidate instance exists, display a message to the user
            messages.warning(request, "You have already submitted your candidate details.")
            return redirect('/candidate-personal-details-update/')  
        except Candidate.DoesNotExist:
            pass
        if request.method=='POST':
            form=CandidateDetailsForm(request.POST,request.FILES)
            if form.is_valid():
                Name=form.cleaned_data['Name']
                DOB=form.cleaned_data['DOB']
                mobile=form.cleaned_data['mobile']
                Experience=form.cleaned_data['Experience']
                Location=form.cleaned_data['Location']
                Resume=form.cleaned_data['Resume']
                user_obj=Candidate(Name=Name,DOB=DOB,mobile=mobile,Experience=Experience,Location=Location,Resume=Resume)
                user_obj.save()
                user_obj.user=request.user
                user_obj.save()
                messages.success(request, "Your candidate details have been saved successfully.")
                return render(request,'Candidate/candidat_details.html',{'form':form})

                    
                
        else:
            form=CandidateDetailsForm()
        return render(request,'Candidate/candidat_details.html',{'form':form})
    else:
        return redirect('/login-Candidate/')



def Candidate_detail_update(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            data_id = request.session.get('data')
            user_candidate = Candidate.objects.get(id=data_id)
            form = CandidateDetailsForm(request.POST, instance=user_candidate)
            if form.is_valid():
                form.save()
                messages.success(request, "Your candidate details have been updated successfully.")
                # print(messages.get_messages(request))  
                return render(request, 'Candidate/Candidate_detail_update.html', {'form': form})
        else:
            data_id = request.session.get('data')
            user_candidate = Candidate.objects.get(id=data_id)
            form = CandidateDetailsForm(instance=user_candidate)
        return render(request, 'Candidate/Candidate_detail_update.html', {'form': form})
    else:
        return redirect('/login-Candidate/')



def Applyfunction(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ApplyForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data['message']
                candidate_data = Candidate.objects.filter(user=request.user).first()
                if candidate_data:
                    recruiter_data = get_object_or_404(Recruiter, pk=id)
                    # Check if the candidate has already applied for this job
                    existing_application = Apply.objects.filter(jobseeker=candidate_data, Recruit=recruiter_data).exists()
                    if not existing_application:
                        user_obj = Apply(message=message, Recruit=recruiter_data, jobseeker=candidate_data, user=request.user)
                        user_obj.save()
                        print('ok')
                        return redirect('/')  # Redirect to a success page after successful application
                    else:
                        # Handle the case where the candidate has already applied for this job
                        return render(request,'home/already_Apply.html')  # Redirect to a page with an error message
                else:
                    # Handle the case where candidate_data is not found for the user
                    return redirect('/candidate-personal-details/')
        else:
            form = ApplyForm()
        return render(request, 'home/apply.html', {'form': form})
    else:
         return redirect('/login-Candidate/')


def Apply_details_fun(request,id):
    if request.user.is_authenticated:
        recruiter_instance = Recruiter.objects.get(pk=id)
        candidates= Candidate.objects.filter(apply__Recruit=recruiter_instance)

        return render(request,'Hr/candidate_apply_list.html',{'candidates':candidates,'recruiter_instance':recruiter_instance })
    else:
        return redirect('/login-hr/')
