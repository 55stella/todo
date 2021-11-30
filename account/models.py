from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    address = models.TextField(null=True, blank= True)
    email= models.EmailField(max_length=50)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    #email =  models.EmailField(max_length=60)


    def __str__(self):
         return self.username
