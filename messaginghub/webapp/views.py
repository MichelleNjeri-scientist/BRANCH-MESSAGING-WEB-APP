import csv
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateAgentResponsesForm, CreateMessageForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import ClientMessages, AgentResponses

from django.contrib import messages
import pandas as pd
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.utils import timezone



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

# - Create a Message

def create_message(request):
    if request.method == "POST":
        form = CreateMessageForm(request.POST)
        
        if form.is_valid():
            message_body = form.cleaned_data['message_body']

            client_message = ClientMessages(
                client_user_id=779,
                message_body=message_body,
                priority='high' if any(keyword in message_body.lower() for keyword in ["loan", "batch"]) else 'normal',
                created_at=timezone.now(),
                status='unread'
            )
            client_message.save()

            messages.success(request, "Your message was sent!")
            return redirect("create-message")
        else:
            # Form is not valid, so there are errors
            messages.error(request, 'Please correct the errors below.')

            

    else:
        form = CreateMessageForm()

    context = {'form': form}
    return render(request, 'webapp/create-message.html', context)


# - Create a Response

@login_required(login_url='my-login')
def agent_response(request, pk):

    client_message = get_object_or_404(ClientMessages, id=pk)

    form = CreateAgentResponsesForm()

    if request.method == 'POST':

        
        form = CreateAgentResponsesForm(request.POST)
        if form.is_valid():

            response_body = form.cleaned_data['response_body']
            agent_user = request.user

            form = AgentResponses(
                client_user_id=client_message.client_user_id,
                response_body=response_body,
                created_at=timezone.now(),
                agent_id=agent_user,
                message_id=client_message
            )

            form.save()

            client_message.status = 'read'
            
            client_message.save()

            messages.success(request, "Your response was sent successfully!")

            return redirect("dashboard")
        
    context = {'client_message': client_message, 'form': form}

    return render(request, 'webapp/agent-response.html', context=context)

# - Read / View a singular user record

@login_required(login_url='my-login')
def singular_user(request, client_user_id):

    client_messages = ClientMessages.objects.filter(client_user_id=client_user_id).order_by('created_at').values()
    agent_responses = AgentResponses.objects.filter(client_user_id=client_user_id)
    return render(request, 'webapp/singular-user.html', {'client_messages': client_messages, 'agent_responses': agent_responses, 'client_user_id': client_user_id})



# - import excel

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





