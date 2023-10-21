from django.contrib.auth.models import User
from django.db import models
    
class ClientMessages(models.Model):

   client_user_id = models.CharField(max_length=20) 
   message_body =  models.TextField()
   created_at = models.DateTimeField()
   priority = models.CharField(max_length=20, default="1")
   status = models.CharField(max_length=500, default="0")

   def __str__(self):

        return self.client_user_id

class AgentResponses(models.Model):

   agent_id = models.ForeignKey(User, on_delete=models.RESTRICT)
   client_user_id = models.CharField(max_length=20)
   message_id = models.ForeignKey(ClientMessages, on_delete=models.RESTRICT)
   response_body =  models.TextField()
   created_at = models.DateTimeField()
   priority = models.CharField(max_length=20)

   def __str__(self):

        return self.client_user_id
   













