from django.db import models
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
    donation_description=models.CharField(max_length=500)
    purpose=models.CharField(max_length=50)
    required_amount=models.IntegerField(default=0)
    recieved_amount=models.IntegerField(default=0)

   
class feedbacks(models.Model):
    fu_name=models.CharField(max_length=50)
    fu_email=models.EmailField( max_length=254)
    fu_message=models.CharField( max_length=300)


# class Supporters(models.Model):
#     user_fullname=models.ForeignKey(Users,verbose_name=("Registered user name"), on_delete=models.CASCADE)
#     user_age=models.ForeignKey(Users, verbose_name=("users age"), on_delete=models.CASCADE)

