from django.urls import path
from . import views

app_name = "dm"
urlpatterns = [
    path('', views.home, name="home"),
    path('gen_guidelines/', views.gen_guidelines, name="gen_guidelines"),
    path('login/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signup/volunteer', views.signup_volunteer, name="signup_vol"),
    path('signup/organization', views.signup_org, name="signup_org"),
    path('logout/', views.logout_user, name="logout"),
]