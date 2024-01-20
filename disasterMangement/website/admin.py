from django.contrib import admin
from .models import myUser,Admin,Volunteer,Organization
# Register your models here.

admin.site.register(myUser)
admin.site.register(Admin)
admin.site.register(Volunteer)
admin.site.register(Organization)
