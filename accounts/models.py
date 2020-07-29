import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_office  = models.BooleanField(default=False)




class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Office(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Balance(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(default=100)
    contact= models.CharField(max_length=120)


class Transaction(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    user   =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='transaction_user')
    to_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount=models.IntegerField()
    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)
        last_bal = Balance.objects.filter(user=self.user).latest('date')
        last_bal_to_user =Balance.objects.filter(user=self.to_user).latest('date')
        Balance.objects.create(date=datetime.datetime.now(), user=self.user, balance=last_bal.balance - self.amount, contact=last_bal.contact)
        Balance.objects.create(date=datetime.datetime.now(), user=self.to_user, balance=last_bal_to_user.balance + self.amount, contact=last_bal_to_user.contact)




class Payment(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=120)
    amount=models.IntegerField()
    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)
        last_bal = Balance.objects.filter(user=self.user).latest('date')
        Balance.objects.create(date=datetime.datetime.now(), user=self.user, balance=last_bal.balance + self.amount, contact=last_bal.contact)



class Employee_spending(models.Model):
    user        =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date        =models.DateTimeField(auto_now_add=True, blank=True)
    name        =models.CharField(max_length=40)
    description =models.CharField(max_length=40)
    quantity    = models.IntegerField(default=1)
    image       =models.ImageField(upload_to='images/',blank=True)
    amount      = models.IntegerField(null=True)
    def save(self, *args, **kwargs):
        super(Employee_spending, self).save(*args, **kwargs)
        last_bal = Balance.objects.filter(user=self.user).latest('date')
        Balance.objects.create(date=datetime.datetime.now(), user=self.user, balance=last_bal.balance - self.amount, contact=last_bal.contact)
