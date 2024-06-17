from django.urls import path
from . import views
from .views import UniqueValuesView, UserSearchView

urlpatterns = [
    path("query-builder/", views.query_builder, name="query_builder"),
    path("unique-values/", UniqueValuesView.as_view(), name="unique-values"),
    path("values/", UserSearchView.as_view(), name="unique-values"),
]
