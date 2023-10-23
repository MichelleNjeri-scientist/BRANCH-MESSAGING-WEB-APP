from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ClientMessages, AgentResponses

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

# - Register/Create a user

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']


# - Login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# - Create a Message

class CreateMessageForm(forms.ModelForm):

    class Meta:

        model = ClientMessages
        fields = ['message_body']
        # fields = ['client_user_id', 'message_body', 'created_at', 'priority', 'status']

# - Update a Response

class CreateAgentResponsesForm(forms.ModelForm):

    class Meta:

        model = AgentResponses
        fields = ['response_body']
        # fields = ['agent_id', 'client_user_id', 'message_id', 'response_body', 'created_at', 'priority']
