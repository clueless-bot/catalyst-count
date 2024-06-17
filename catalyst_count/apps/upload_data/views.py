import os
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .tasks import process_csv_file

@csrf_exempt
def import_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', csv_file.name)
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in csv_file.chunks():
                temp_file.write(chunk)

        process_csv_file.delay(temp_file_path)

        messages.success(request, "CSV file uploaded and processing started.")
        return render(request, "dashboard.html")

    else:
        return render(request, "dashboard.html")
