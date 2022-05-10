from django.urls import path
# from .views import FavList
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path("", FavList.as_view(), name="favorites"),
]

urlpatterns += staticfiles_urlpatterns()