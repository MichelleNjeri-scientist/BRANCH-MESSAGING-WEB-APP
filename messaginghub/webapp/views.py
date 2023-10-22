import csv
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record, ClientMessages

from django.contrib import messages
import pandas as pd
from datetime import datetime



# - Homepage 

def home(request):

    return render(request, 'webapp/index.html')


# - Register a user

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)

"""
# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)
"""

# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):
    context = {}
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None

        if start_date and end_date:
            my_client_messages = ClientMessages.objects.filter(created_at__range=(start_date, end_date))
        else:
            my_client_messages = ClientMessages.objects.all()
        # Define a custom sorting key
        def custom_sort_key(client_message):
            if 'loan' in client_message.message_body:
                return (0, client_message.message_body)
            elif 'batch' in client_message.message_body:
                return (0, client_message.message_body)
            else:
                return (1, client_message.message_body)

        # Sort the queryset based on the custom sorting key
        sorted_client_messages = sorted(my_client_messages, key=custom_sort_key)
        context = {'client_messages': sorted_client_messages}

    # ClientMessages.objects.all().delete() 

    return render(request, 'webapp/dashboard.html', context=context)

    # return render(request, 'webapp/dashboard.html')

# - Create a record 

@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")

            return redirect("dashboard")

    context = {'form': form}

    return render(request, 'webapp/create-record.html', context=context)


# - Update a record 

@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-record.html', context=context)


# - Read / View a singular record

@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html', context=context)


# - Delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")



def import_excel_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        try:
            for index, row in df.iterrows():
                ClientMessages.objects.create(
                    client_user_id=row['client_user_id'],
                    created_at=row['created_at'],
                    message_body=row['message_body'],
                )
            messages.success(request, 'EXCEL file imported successfully.')
        except Exception as e:
            messages.error(request, f'Error importing EXCEL: {str(e)}')
    return render(request, 'webapp/import-excel.html')



# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")





