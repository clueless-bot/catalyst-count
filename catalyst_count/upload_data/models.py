# models.py

from django.db import models


class Data(models.Model):
    unknown_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    domain = models.CharField(max_length=255, null=True)
    year_founded = models.IntegerField(null=True)
    industry = models.CharField(max_length=255, null=True)
    size_range = models.CharField(max_length=100, null=True)
    locality = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=100, null=True)
    linkedin_url = models.URLField(null=True)
    current_employee_estimate = models.IntegerField(null=True)
    total_employee_estimate = models.IntegerField(null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
