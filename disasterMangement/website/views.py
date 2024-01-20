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
def signin(request):
    if request.method == "POST":
        userType = request.POST['userType']
        if userType == 'volunteer':
            return render(request, 'signin_vol.html')
        else:
            return render(request, 'signin_org.html')
        
    return render(request, 'signin.html')

def signin_volunteer(request):
    if request.method == "POST":
        form = Signin_Form(request.POST)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if user.user_role == myUser.Volunteer:
                login(request, user)
                messages.info(request,"You have logged in successfully!!")
                return redirect('home')
            else:
                messages.error(request,"You are not a volunteer. Redirecting to organization login page...")
                return redirect('signin_org')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
        
    form = Signin_Form()
    return render(request, 'signin_vol.html', {
        "form":form
        })

def signin_org(request):
    if request.method == "POST":
        form = Signin_Form(request.POST)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if user.user_type == myUser.Volunteer:
                login(request, user)
                messages.info(request,"You have logged in successfully!!")
                return redirect('home')
            else:
                messages.error(request,"You are not an organizatoin. Redirecting to volunteer login page...")
                return redirect('signin_volunteer')                
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    
    form = Signin_Form()
    return render(request, 'signin_org.html', {
        "form":form
    })

def logout_user(request):
    logout(request)
    messages.info(request,"You have logged out!!")
    return redirect('home')


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
                return redirect('signup_volunteer')
            
            if password1 != password2:
                messages.error(request,"Provided passwords don't match")
                return redirect('signup_volunteer')
            
            user_type = email.split('@')[1].split('.')[1]
            if user_type not in myUser.Email_To_User_Map:
                messages.error(request, "The provided email id seems invalid")
                return redirect('signup_volunteer')

            email_exists = Volunteer.objects.filter(email=email).exists()
            if email_exists:
                messages.error(request, 'User with this email id already exists. Please proceed to login!!')
                return redirect('signin_volunteer')
            
            user = myUser(username=username, email=email)
            user.set_password(password1)
            user.user_role = myUser.Volunteer
            user.save()

            volunteer = Volunteer(user=user, first_name=first_name, last_name=last_name, age=age, nationality=nationality, email=email)
            volunteer.save()
            return redirect('signin_volunteer')
        else:
            messages.error(request,"Please fill all the details")
            return redirect('signup_volunteer')
    
    form = Signup_Volunteer()
    return render(request, 'signup_vol.html',{
        "form":form
    })


def signup_org(request):
    if request.method == 'POST':
        form = Signup_Org(request.POST)
        username = form.cleaned_data["username"]
        org_name = form.cleaned_data["org_name"]
        org_type = form.cleaned_data["org_type"]
        org_email = form.cleaned_data["org_email"]
        password1 = form.cleaned_data["password1"]
        password2 = form.cleaned_data["password2"]

        if not (form.is_valid()):
            messages.error(request,"Please fill all the details")
            return redirect('signup_org')
        
        username_exists = myUser.objects.filter(username=username).exists()
        if username_exists:
            messages.error(request, 'User with this username already exists. Please try another username!!')
            return redirect('signup_volunteer')
        
        if password1!=password2:
            messages.error(request,"Provided passwords don't match")
            return redirect('signup_volunteer')
        
        user_type = org_email.split('@')[1].split('.')[1]
        if user_type not in myUser.Email_To_User_Map:
            messages.error(request, "The provided email id seems invalid")
            return redirect('signup_volunteer')

        email_exists = Volunteer.objects.filter(email=org_email).exists()
        if email_exists:
            messages.error(request, 'User with this email id already exists. Please proceed to login!!')
            return redirect('signin_volunteer')
        
        user = myUser(username=username, email=org_email)
        user.set_password(password1)
        user.user_role = myUser.Organization
        user.save()

        org = Organization(user=user, org_name=org_name,org_type=org_type,org_email=org_email)
        org.save()
        return redirect('signin_org')
    
    form = Signup_Org()
    return render(request, 'signup_org.html',{
        "form":form
    })

