from asyncio.windows_events import NULL
from pickle import TRUE
from django import views
from django.http import HttpResponse
from django.shortcuts import render,redirect
from crowdfunding.models import Donation,  feedbacks
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


# about page
def about_page(request):
    if User.is_authenticated:
        uinf=userinfo(request)
        uid=uinf.username

    return render(request,'about.html',{'uname':uid})


# contact page
def contact_page(request):
    uid=userinfo(request).username
    if request.method=="POST":
        fname=request.POST["fullname"]
        femail=request.POST['email']
        fmessage=request.POST['message']
        savemessage=feedbacks(fu_name=fname,fu_email=femail,fu_message=fmessage)
        savemessage.save()
        return redirect('home.html')


    return render(request,'contact.html',{'uname':uid})


# all donations
def donate_now_page(request):
    aprv_data=adata(request)
    uid=userinfo(request).username

    return render(request,'donation.html',{'ad':aprv_data,'uname':uid})

# success stories
def success_stories(request):
    s_data=Donation.objects.filter(donation_status='s')
    uid=userinfo(request).username
    return render(request,'success_stories.html',{'sd':s_data,'uname':uid})


#req donation
def req_donation_page(request):
    if request.method=='POST':
        fname=request.POST['full_name']
        email=request.POST['email']
        mob=request.POST['mobile_number']
        address=request.POST['address']
        title=request.POST['donation_title']
        desc=request.POST['description']
        purpose=request.POST['purpose']
        amount=request.POST['donation_ammount']
        # thumbnail=request.POST['donation_image']
        image=request.POST['donation_image']
        post=Donation(full_name=fname,email=email,phone=mob,address=address,donation_title=title,donation_description=desc,purpose=purpose,required_amount=amount,image=image)
        post.save()
        return redirect('req-donation')

    uid=userinfo(request).username


    return render(request,'req_donation.html',{'uname':uid})


#login
def login_form(request):
    if request.method=='POST':
        uname=request.POST['email']
        passw=request.POST['password']
        user=authenticate(username=uname,password=passw)
        if user is not None:
            login(request,user)
            uname=user.get_username
            return redirect('home')
    if request.user.is_authenticated==TRUE:
        return redirect('home')
    else:
        return render(request,'login.html')

#register 
def register_user(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can log in now!')    
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}


    return render(request, 'register.html',context)

# logout
@login_required
def logout_user(request):
    if User.is_authenticated:
        logout(request)
        return redirect('home')

def home_page(request):
    aprv_data=adata(request)
    s_data=sdata(request)
    uid=userinfo(request).username
        
    return render(request,'home.html',{'sd':s_data,'ad':aprv_data,'uname':uid})

def adata(request):
    data=Donation.objects.filter(donation_status='a')
    return(data)

def sdata(request):
    data=Donation.objects.filter(donation_status='s')
    return(data)

def userinfo(request):
    if User.is_authenticated:
        userinf=request.user
        return(userinf)

def donations_details(request,id):
    data=Donation.objects.get(id=id)
    others=Donation.objects.filter(donation_status='a')
    uid=userinfo(request).username
    return render(request,'fullpost.html',{'ob':others,'inf':data,'uname':uid})



    