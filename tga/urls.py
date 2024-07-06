from django.urls import path
from .views import mount_data
urlpatterns =[
    path('',mount_data),
]