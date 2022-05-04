from asyncio.windows_events import NULL
from multiprocessing.sharedctypes import Value
from pickle import TRUE
from django import views
from django.forms import EmailInput
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from crowdfunding.models import Donation,  feedbacks, public_donors, topdonors, transactions
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

# home page
def home_page(request):
    aprv_data=adata(request)
    s_data=sdata(request)
    uid=userinfo(request).username
        
    return render(request,'home.html',{'sd':s_data,'ad':aprv_data,'uname':uid})

#retriving approved data   
def adata(request):
    data=Donation.objects.filter(donation_status='a')
    return(data)

#retriving donation completed data      
def sdata(request):
    data=Donation.objects.filter(donation_status='s')
    return(data)


#getting user info
def userinfo(request):
    if User.is_authenticated:
        userinf=request.user
        return(userinf)


#donation details post from donates page
def donations_details(request,slugs):
    data=Donation.objects.get(slugs=slugs)
    others=Donation.objects.filter(donation_status='a')
    uid=userinfo(request)
    
    if request.method == "POST":
        if request.user.is_authenticated==True:
            did=request.POST['donation-id']
            amount=int(request.POST['amount'])
            uuid=request.user.id

            update_amt_donation=Donation.objects.filter(id=did).get()
            update_amt_donation.recieved_amount=int(update_amt_donation.recieved_amount)+int(amount)
            update_amt_donation.save()
            update_amt_status=Donation.objects.filter(id=did).get()
            try:
                res=update_amt_status.if_success()
                update_amt_status.save()
                print(res)
            except:
                print('failed to run status function')

            try:
                obj=topdonors.objects.filter(uid=uuid).get()
                obj.total_amount=obj.total_amount+amount
                obj.save()
            except :
                add_contribution=topdonors(uid=uuid,status='user',total_amount=amount)
                add_contribution.save()

            post_transaction=transactions(did=did,uid=uuid,amount=amount)
            post_transaction.save()
        else:
            did=request.POST['donation-id']
            name=request.POST['fullname']
            phone=request.POST['phone']
            emails=request.POST['email']
            address=request.POST['address']
            amount=request.POST['amount']

            #update amount in donation post 
            update_amt_donation=Donation.objects.filter(id=did).get()
            update_amt_donation.recieved_amount=int(update_amt_donation.recieved_amount)+int(amount)
            update_amt_donation.save()
            update_amt_status=Donation.objects.filter(id=did).get()
            try:
                res=update_amt_status.if_success()
                update_amt_status.save()
                print(res)
            except:
                print('failed to run status function')

            try:
                obj=public_donors.objects.filter(email=emails).get() 
                print(obj.id,'obj id public donor') 
                td_obj=topdonors.objects.get(pid=obj.id)
                td_obj.total_amount=int(td_obj.total_amount)+int(amount)
                td_obj.save()
                print('updated topdonors')
                print(obj.id)
                add_transaction=transactions(pid=obj.id,amount=amount,did=did)
                add_transaction.save()
                print('transaction')
            except:
                add_donor=public_donors(name=name,email=emails,address=address,phone=phone)
                add_donor.save()
                print("new public donor")
                get_donorid=public_donors.objects.filter(email=emails).get()
                print(get_donorid.id)
                add_topdonor=topdonors(pid=get_donorid.id,total_amount=amount,status='unregistered')
                add_topdonor.save()
                print('added to topdonor')
                add_transaction=transactions(pid=add_donor.id,amount=amount,did=did)
                add_transaction.save()
                print('transaction')

    return render(request,'fullpost.html',{'ob':others,'inf':data,'uname':uid})

