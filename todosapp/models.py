from datetime import datetime
from django.db import models

from django.utils import timezone
from account.models import CustomUser
from django .contrib.auth import get_user_model

# def get_day():
#     date = timezone.now()
#     day = datetime.strftime(date,"%a-%d-%b-%Y")
#     return day

# Create your models here.
User = get_user_model()
class Todos(models.Model):
    user = models.ForeignKey(User, on_delete =models.CASCADE,related_name='to_do', max_length=100, null= True, blank=True)
    activity = models.CharField(max_length=350, null=True, blank=True)
    completed = models.BooleanField(default=False)
    date = models.DateField(datetime.now)
    note = models. CharField(max_length=300)
    created = models.DateField(auto_now_add=True, )



    def __str__(self):
        return f'{self.activity }for {self.user.username}'
        

    def __str__(self):
        return self.activity


        
        


