# views.py

import os
import csv
from tempfile import TemporaryFile
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CSVUploadForm
from .models import Data
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def import_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]

        # Create a temporary file to stream the upload
        with TemporaryFile() as temp_file:
            for chunk in csv_file.chunks():
                temp_file.write(chunk)
            temp_file.flush()  # Ensure all data is written

            # Seek back to the beginning of the file for reading
            temp_file.seek(0)

            # Decode the file and read as CSV
            decoded_file = temp_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                # Convert empty strings to None for nullable fields
                for key in row.keys():
                    if row[key] == "":
                        row[key] = None
                list = row["locality"].split(",")
                Data.objects.create(
                    id=row["id"],
                    name=row["name"],
                    domain=row["domain"],
                    year_founded=row["year founded"],
                    industry=row["industry"],
                    size_range=row["size range"],
                    locality=row["locality"],
                    country=row["country"],
                    linkedin_url=row["linkedin url"],
                    current_employee_estimate=row["current employee estimate"],
                    total_employee_estimate=row["total employee estimate"],
                    city=list[0],
                    state=list[1],
                    
                )

        # Optionally, you can pass additional context to the dashboard.html template
        # For example:
        # context = {
        #     'message': 'CSV file uploaded and data saved successfully.'
        # }
        # return render(request, 'dashboard.html', context)

        # Redirect to the dashboard page after uploading CSV
        return render(request, "dashboard.html")

    else:
        return render(request, "dashboard.html")
