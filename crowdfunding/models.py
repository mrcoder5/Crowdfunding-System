from email.mime import image
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Donation(models.Model):
    status=(
        ('r','request'),
        ('a','approved'),
        ('s','successful'),
        ('x','rejected')
    )

    donation_status=models.CharField(max_length=1,choices=status,default='r')
    full_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    phone=models.IntegerField()
    address=models.CharField( max_length=500)
    donation_title=models.CharField(max_length=100)
    slugs=models.SlugField(max_length=150,unique=True,null=True)
    donation_description=models.CharField(max_length=500)
    purpose=models.CharField(max_length=50)
    required_amount=models.IntegerField(default=0)
    recieved_amount=models.IntegerField(default=0)
    date_and_time=models.DateTimeField(default=timezone.now)
    image=models.ImageField(upload_to='images',null=True)

    
    def progress(self):
        pp=self.recieved_amount / self.required_amount *100
        return pp
        
   
class feedbacks(models.Model):
    fu_name=models.CharField(max_length=50)
    fu_email=models.EmailField( max_length=254)
    fu_message=models.CharField( max_length=300)
    date_and_time=models.DateTimeField(default=timezone.now)


class transactions(models.Model):
    did=models.IntegerField()
    uid=models.IntegerField()
    amount=models.IntegerField(blank=True,null=True)
    date_and_time=models.DateTimeField(default=timezone.now)
    


class topdonors(models.Model):
    did=models.IntegerField()
    uid=models.IntegerField()
    total_amount=models.IntegerField(null=True)
    updated=models.DateTimeField(default=timezone.now)




