from django.shortcuts import render
from django.db import connection


def email_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT email, verified FROM account_emailaddress")
        emails = cursor.fetchall()
    return render(request, "user.html", {"emails": emails})
