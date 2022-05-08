from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.search, name="search"),
    path("result/", views.results, name="result"),
]

urlpatterns += staticfiles_urlpatterns()