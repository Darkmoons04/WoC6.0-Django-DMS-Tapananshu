from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class myUser(AbstractUser):
    Admin = '1'
    Volunteer = '2'
    Organization = '3'
    
    Email_To_User_Map = {
        "admin": Admin,
        "com": Volunteer,
        "org": Organization
    }
    User_Type = ((Admin,"Admin"),(Volunteer,"Volunteer"),(Organization,"Organization"))
    user_role = models.CharField(max_length=20, choices=User_Type)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user_role == "1":
            Volunteer.objects.get_or_create(role=self)
        elif self.user_role == "2":
            Organization.objects.get_or_create(role=self)
        elif self.user_role == "3":
            Admin.objects.get_or_create(role=self)


class Admin(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()

class Volunteer(models.Model):
    role = models.OneToOneField(myUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    age = models.IntegerField()
    nationality = models.CharField(max_length=25)
    email = models.EmailField()

class Organization(models.Model):
    Org_type = (("PRIVATE","private"),("GOVT.","government"),("SEMI GOVT.","semi_govt"))
    role = models.OneToOneField(myUser, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=30)
    org_type = models.CharField(max_length=20, choices=Org_type, blank=False)
    org_email = models.EmailField()
    




