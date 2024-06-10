# csv_import/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("import-csv/", views.import_csv, name="import_csv"),
]
