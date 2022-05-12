from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Permet de lier le backend et le frontend à l'aide d'un path URL
urlpatterns = [
    path("", views.favorites, name="favorites"),
]

urlpatterns += staticfiles_urlpatterns()