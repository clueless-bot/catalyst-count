from django.urls import path
from . import views

urlpatterns = [
    path("email-list/", views.email_list, name="email-list"),
]
