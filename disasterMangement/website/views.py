from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import Signup_Org,Signup_Volunteer,Signin_Form
from .models import myUser, Volunteer, Organization, Admin

# Create your views here.
def home(request):
    return render(request, 'home.html',{})

def gen_guidelines(request):
    return render(request, 'gen_guidelines.html')


################################# LOGIN Views ##############################
# def signin(request):
#     if request.method == "POST":
#         userType = request.POST['userType']
#         if userType == 'volunteer':
#             return render(request, 'signin_vol.html')
#         else:
#             return render(request, 'signin_org.html')
        
#     return render(request, 'signin.html')

def signin(request):
    form = Signin_Form()
    if request.method == "POST":
        form = Signin_Form(request.POST)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.info(request,"You have logged in successfully!!")
            return redirect('dm:home')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('dm:signin')
        
    return render(request, 'signin.html', {
        "form":form
        })

# def signin_org(request):
#     form = Signin_Form()
#     if request.method == "POST":
#         form = Signin_Form(request.POST)
#         username = form.cleaned_data["username"]
#         password = form.cleaned_data["password"]
#         user = authenticate(request, username = username, password = password)
#         if user is not None:
#             if user.user_type == myUser.Volunteer:
#                 login(request, user)
#                 messages.info(request,"You have logged in successfully!!")
#                 return redirect('dm:home')
#             else:
#                 messages.error(request,"You are not an organizatoin. Redirecting to volunteer login page...")
#                 return redirect('signin_vol')                
#         else:
#             messages.info(request,"Invalid Credentials")
#             return redirect('dm:signin')

#     return render(request, 'signin_org.html', {
#         "form":form
#     })

def logout_user(request):
    logout(request)
    messages.info(request,"You have logged out!!")
    return redirect('dm:home')


################################# REGISTER Views ##############################
def signup(request):
    if request.method == "POST":
        type = request.POST['userType']
        if type == 'volunteer':
            return render(request, 'signup_vol.html')
        else:
            return render(request, 'signup_org.html')
        
    return render(request, 'signup.html')

  
def signup_volunteer(request):
    form = Signup_Volunteer()
    if request.method == 'POST':
        form = Signup_Volunteer(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            age = form.cleaned_data["age"]
            nationality = form.cleaned_data["nationality"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            username_exists = myUser.objects.filter(username=username).exists()
            if username_exists:
                messages.error(request, 'User with this username already exists. Please try another username!!')
                return redirect('dm:signup_vol')
            
            if password1 != password2:
                messages.error(request,"Provided passwords don't match")
                return redirect('dm:signup_vol')
            
            user_type = email.split('@')[1].split('.')[1]
            if user_type not in myUser.Email_To_User_Map:
                messages.error(request, "The provided email id seems invalid")
                return redirect('dm:signup_vol')

            email_exists = Volunteer.objects.filter(email=email).exists()
            if email_exists:
                messages.error(request, 'User with this email id already exists. Please proceed to login!!')
                return redirect('dm:signin_vol')
            
            user = myUser(username=username)
            user.set_password(password1)
            user.user_role = myUser.Volunteer
            user.save()

            volunteer = Volunteer(role=user.user_role, first_name=first_name, last_name=last_name, age=age, nationality=nationality, email=email)
            volunteer.save()
            return redirect('dm:signin_vol')
        
        else:
            messages.error(request,"Please...fill all the details")
            print(form.errors)
            return redirect('dm:signup_vol')
    
    return render(request, 'signup_vol.html',{
        "form":form
    })


def signup_org(request):
    if request.method == 'POST':
        form = Signup_Org(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            org_name = form.cleaned_data["org_name"]
            org_type = form.cleaned_data["org_type"]
            org_email = form.cleaned_data["org_email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            username_exists = myUser.objects.filter(username=username).exists()
            if username_exists:
                messages.error(request, 'User with this username already exists. Please try another username!!')
                return redirect('dm:signup_org')
            
            if password1 != password2:
                messages.error(request,"Provided passwords don't match")
                return redirect('dm:signup_org')
            
            user_type = org_email.split('@')[1].split('.')[1]
            if user_type not in myUser.Email_To_User_Map:
                messages.error(request, "The provided email id seems invalid")
                return redirect('dm:signup_org')

            email_exists = Volunteer.objects.filter(email=org_email).exists()
            if email_exists:
                messages.error(request, 'User with this email id already exists. Please proceed to login!!')
                return redirect('dm:signin_org')
            
            user = myUser(username=username)
            user.set_password(password1)
            user.user_role = myUser.Organization
            user.save()

            org = Organization(role=user.user_role, org_name=org_name, org_type=org_type, org_email=org_email)
            org.save()
            return redirect('dm:signin_org')
        
        else:
            messages.error(request,"Please...fill all the details")
            return redirect('dm:signup_org')
    
    else:
        form = Signup_Org()
    
    return render(request, 'signup_org.html', {"form": form})

