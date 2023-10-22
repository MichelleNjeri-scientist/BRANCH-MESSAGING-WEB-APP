from django.contrib.auth.models import User
from django.db import models

class Record(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=255)

    province = models.CharField(max_length=200)

    country = models.CharField(max_length=125)


    def __str__(self):

        return self.first_name + "   " + self.last_name
    
class ClientMessages(models.Model):

   client_user_id = models.CharField(max_length=20) 
   message_body =  models.TextField()
   created_at = models.DateTimeField()
   priority = models.CharField(max_length=20, default="normal")
   status = models.CharField(max_length=500, default="unread")

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
   













