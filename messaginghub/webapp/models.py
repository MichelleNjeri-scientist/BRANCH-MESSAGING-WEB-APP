from django.contrib.auth.models import User
from django.db import models
    
class ClientMessages(models.Model):

   client_user_id = models.CharField(max_length=20) 
   message_body =  models.TextField()
   created_at = models.DateTimeField()
   priority = models.CharField(max_length=20, default="normal")
   status = models.CharField(max_length=500, default="unread")

   def __str__(self):

        return self.message_body

class AgentResponses(models.Model):

   agent_id = models.ForeignKey(User, on_delete=models.CASCADE)
   client_user_id = models.CharField(max_length=20)
   message_id = models.ForeignKey(ClientMessages, on_delete=models.CASCADE)
   response_body =  models.TextField()
   created_at = models.DateTimeField()

   def __str__(self):

        return self.response_body
   













