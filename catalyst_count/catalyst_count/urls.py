from django.contrib import admin
from django.urls import path, include
from .views import get_csrf_token
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/csrf/", get_csrf_token, name="get_csrf_token"),
    path("accounts/signup/", views.signup_view, name="signup"),
    path("accounts/login/", views.login_view, name="login"),
    path("", views.dashboard_view, name="dashboard"),
    path("csv/", include("upload_data.urls")),
    path("filter/", include("query_builder.urls")),
    path("users/", include("users.urls")),
]
