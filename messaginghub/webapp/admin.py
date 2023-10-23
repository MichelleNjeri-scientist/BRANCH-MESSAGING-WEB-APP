from django.contrib import admin

# Register your models here.
from .models import ClientMessages, AgentResponses

admin.site.register(ClientMessages)
admin.site.register(AgentResponses)