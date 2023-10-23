# BRANCH MESSAGING WEB APP
 BRANCH MESSAGING WEB APP

 This is a python based web application that can be used to simulate client/user messages, responses by customer service agents and importing of message data on excel.

 # HOW TO INSTALL
Once you have python installed on your machine. You can open your desired terminal and go to the directory where your dev files are and run the following commands to get you set up.
 
pip install virtualenv
pip install django
pip install django-crispy-forms==1.14.0
pip install pandas
pip install openpyxl
pip list

virtualenv branchatenv
branchatenv\Scripts\activate


django-admin startproject messaginghub 
cd messaginghub

django-admin startapp webapp
go to  messaginghub/settings.py on your file explorer and add webapp to INSTALLED_APPS

go back to your terminal and run the following:
python manage.py makemigrations
python manage.py migrate
python migrate.py createsuperuser 


Once you create your django admin account you are now ready to roll!!!

Copy all the files in this repo to your project and run the following in your terminal:
python manage.py runserver

Go to http://127.0.0.1:8000 on your browser!!!

# WHAT GOALS WERE ACHIEVED!!

1. Created a messaging web application that can be used to respond to incoming questions sent by customers. The system allows a team of agents to respond to incoming messages from (potentially many) customers in a streamlined fashion. 
2.	The customer messages can be sent and received through an API endpoint which is simulated via a simple web form.
3.	Store CSV file messages in a database .These messages appear on the agents portal and they can view and respond to these individual messages.
4.	Host my application on my machine.
5.	Explored ways to surface messages that are more urgent and in need of immediate attention.
6. Implemented search functionality to allow agents to search over incoming messages and / or customers

# IMPORTANT CODES USED TO ACHIEVE THE GOAL!!
# 1. Sorting the messages according to key words where those that match are high priority ex (batch and loan) and the rest are normal priority.
# 2. Searching messages according to the dates.
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

    return render(request, 'webapp/dashboard.html', context=context)

# 3. Client message priority is set according to whether any word within the message body matches the key words or not.

priority='high' if any(keyword in message_body.lower() for keyword in ["loan", "batch"]) else 'normal',


