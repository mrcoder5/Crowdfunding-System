
from multiprocessing import set_forkserver_preload
from tkinter import CASCADE
from typing import Iterable
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Donation(models.Model):
    status=[
        ('r','requested'),
        ('a','approved'),
        ('s','successful'),
        ('x','rejected')
    ]
    uid=models.ForeignKey(User, verbose_name="User Id", on_delete=models.CASCADE,null=True)
    donation_status=models.CharField(max_length=1,choices=status,default='r')
    full_name=models.CharField(max_length=50,null=True)
    email=models.EmailField(max_length=254,null=True)
    phone=models.IntegerField(null=True)
    address=models.CharField( max_length=500,null=True)
    donation_title=models.CharField(max_length=100)
    slugs=models.SlugField(max_length=150,unique=True,null=True)
    donation_description=models.CharField(max_length=500)
    purpose=models.CharField(max_length=50)
    required_amount=models.IntegerField(default=0)
    recieved_amount=models.IntegerField(default=0)
    date_and_time=models.DateTimeField(default=timezone.now)
    image=models.ImageField(upload_to='images',null=True)

    def max_rec_amt(self):
        max_amt=self.required_amount-self.recieved_amount
        return max_amt
    
    def progress(self):
        pp=self.recieved_amount / self.required_amount *100
        return pp

    def if_success(self):
        if self.donation_status=='a':
            if self.recieved_amount==self.required_amount:
                self.donation_status='s'
                return self.status

   
class feedbacks(models.Model):
    fu_name=models.CharField(max_length=50)
    fu_email=models.EmailField( max_length=254)
    fu_message=models.CharField( max_length=300)
    date_and_time=models.DateTimeField(default=timezone.now)


class public_donors(models.Model):
    name=models.CharField(max_length=50)
    phone=models.IntegerField()
    address=models.CharField(max_length=250)
    email=models.EmailField(max_length=254,unique=True)


class transactions(models.Model):
    # did=models.IntegerField()
    did=models.ForeignKey(Donation, on_delete=models.CASCADE,null=True,verbose_name="Donation id")
    uid=models.ForeignKey(User, verbose_name="user id", on_delete=models.DO_NOTHING,null=True)
    pid=models.ForeignKey(public_donors, verbose_name="unregistered user id", on_delete=models.DO_NOTHING,null=True)
    amount=models.IntegerField(blank=True,null=True)
    visibility=models.CharField(max_length=3,default='yes')
    date_and_time=models.DateTimeField(default=timezone.now)

class topdonors(models.Model):
    uid=models.ForeignKey(User, verbose_name="user id", on_delete=models.DO_NOTHING ,null=True)
    pid=models.ForeignKey(public_donors, verbose_name="unregistered user id", on_delete=models.DO_NOTHING,null=True)
    status=models.CharField(max_length=50,null=True)
    total_amount=models.IntegerField(default=0)
    visibility=models.CharField(max_length=3,default='yes')
    pos=models.TextField(null=True)
    updated=models.DateTimeField(default=timezone.now)


class pos(models.Model):
    tag=models.TextField(default='')
    posno=models.IntegerField()
    css_class=models.TextField(null=True)

