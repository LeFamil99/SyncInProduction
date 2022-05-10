from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.favorites, name="favorites"),
]

urlpatterns += staticfiles_urlpatterns()