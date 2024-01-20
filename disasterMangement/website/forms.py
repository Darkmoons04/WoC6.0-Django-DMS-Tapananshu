from django.forms import forms
from .models import myUser, Volunteer, Organization
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class Signin_Form(AuthenticationForm):
    class Meta:
        model = myUser
        fields = ['username','password']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
        }

############################################ Sign up forms ##############################
class Signup_Volunteer(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    age = forms.IntegerField()
    nationality = forms.CharField(max_length=30)

    class Meta:
        model = myUser
        fields = ['username', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'age': forms.NumberInput(attrs={'class':'form-control'}),
            'nationality': forms.TextInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }

class Signup_Org(UserCreationForm):
    org_name = forms.CharField(max_length=30)
    org_type = forms.ChoiceField(choices=Organization.Org_type)
    org_email = forms.EmailField()

    class Meta:
        model = myUser
        fields = ['username', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'org_email': forms.TextInput(attrs={'class':'form-control'}),
            'org_name': forms.TextInput(attrs={'class':'form-control'}),
            'org_type': forms.Select(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }




