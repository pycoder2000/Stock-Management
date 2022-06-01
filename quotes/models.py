from django.db import models
from django.contrib.auth.models import User
from django.db.models import *
# Create your models here.
class Stock(models.Model):
    ticker = CharField(max_length=10)
    user = ForeignKey(User,on_delete=CASCADE,default=None,null=True)    
    def __str__(self):
        return self.ticker
