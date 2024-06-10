from django.shortcuts import render

# Create your views here.
def query_builder(request):
    return render(request, "query.html")


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Min, Max
from upload_data.models import Data
from .serializers import UniqueValuesSerializer
from django.db.models import Q


class UniqueValuesView(APIView):
    def get(self, request):
        industries = Data.objects.values_list("industry", flat=True).distinct()
        years_founded = Data.objects.values_list(
            "year_founded", flat=True
        ).distinct()
        cities = Data.objects.values_list("city", flat=True).distinct()
        states = Data.objects.values_list("state", flat=True).distinct()
        countries = Data.objects.values_list("country", flat=True).distinct()

        total_employee_estimates = Data.objects.aggregate(
            total_employee_min=Min("total_employee_estimate"),
            total_employee_max=Max("total_employee_estimate"),
        )

        data = {
            "industries": industries,
            "years_founded": years_founded,
            "cities": cities,
            "states": states,
            "countries": countries,
            **total_employee_estimates,
        }

        serializer = UniqueValuesSerializer(data)

        return Response(serializer.data)


class UserSearchView(APIView):
    def get(self, request):
        # Get query parameters from request
        keyword = request.query_params.get("keyword", "")
        industry = request.query_params.get("industry", "")
        year_founded = request.query_params.get("year_founded", "")
        city = request.query_params.get("city", "")
        state = request.query_params.get("state", "")
        country = request.query_params.get("country", "")
        employees_from = request.query_params.get("employees_from", "")
        employees_to = request.query_params.get("employees_to", "")

        
        

        
        queryset = Data.objects.all()

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(domain__icontains=keyword)
            )

        if industry:
            queryset = queryset.filter(industry__icontains=industry)

        if year_founded:
            queryset = queryset.filter(year_founded=year_founded)

        if city:
            queryset = queryset.filter(city__icontains=city)

        if state:
            queryset = queryset.filter(state__icontains=state)

        if country:
            queryset = queryset.filter(country__icontains=country)

        if employees_from and employees_to:
            queryset = queryset.filter(
                total_employee_estimate__gte=employees_from,
                total_employee_estimate__lte=employees_to,
            )

        
        # print(queryset.query)

        
        user_count = queryset.count()

        return Response({"user_count": user_count})
