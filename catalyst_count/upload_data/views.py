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
    if request.method == "POST" and request.FILES.get("csv_file"):
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
                row["year founded"] = int(row["year founded"]) if row["year founded"].isdigit() else 0

                # Handle numeric fields and ensure they are properly converted
                def safe_int(value):
                    try:
                        return int(value) if value else 0
                    except (ValueError, TypeError):
                        return 0  # Default to 0 if conversion fails

                current_employee_estimate = safe_int(row.get("current employee estimate", "0"))
                total_employee_estimate = safe_int(row.get("total employee estimate", "0"))

                # Handle locality splitting safely
                locality = row.get("locality", "")
                locality_split = locality.split(",") if locality else []
                city = locality_split[0].strip() if len(locality_split) > 0 else None
                state = locality_split[1].strip() if len(locality_split) > 1 else None

                # Create and save the Data object
                Data.objects.create(
                    id=None,
                    name=row["name"] if row["name"] else None,
                    domain=row["domain"] if row["domain"] else None,
                    year_founded=row["year founded"],
                    industry=row["industry"] if row["industry"] else None,
                    size_range=row["size range"] if row["size range"] else None,
                    locality=row["locality"] if row["locality"] else None,
                    country=row["country"] if row["country"] else None,
                    linkedin_url=row["linkedin url"] if row["linkedin url"] else None,
                    current_employee_estimate=current_employee_estimate,
                    total_employee_estimate=total_employee_estimate,
                    city=city,
                    state=state,
                )

        context = {
            'message': 'CSV file uploaded and data saved successfully.'
        }
        return render(request, "dashboard.html", context)

    else:
        return render(request, "dashboard.html")
