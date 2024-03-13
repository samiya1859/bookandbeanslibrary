from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name ="account",on_delete=models.CASCADE)
    account_no = models.IntegerField(unique = True)
    

    def __str__(self) -> str:
        return str(self.name)