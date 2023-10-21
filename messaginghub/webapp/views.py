import csv
from django.shortcuts import render, redirect

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import ClientMessages

from django.contrib import messages



# - Homepage 

def home(request):

    return render(request, 'webapp/index.html')

def import_csv_view(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
        else:
            try:
                with csv_file.open('r') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        ClientMessages.objects.create(
                            client_user_id=row['user_id'],
                            created_at=row['timestamp'],
                            message_body=row['message_body'],
                        )
                messages.success(request, 'CSV file imported successfully.')
            except Exception as e:
                messages.error(request, f'Error importing CSV: {str(e)}')

    return render(request, 'webapp/import-csv.html')







