from django.urls import path
from .views import index
from .api import api

urlpatterns = [
    path("api/", api.urls)
]
