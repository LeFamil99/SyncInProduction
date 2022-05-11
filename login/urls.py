from django.urls import path
from . import views
from .views import Signup, Signin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("signin/", Signin.as_view(), name="signin"),
]

urlpatterns += staticfiles_urlpatterns()