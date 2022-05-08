from asyncio.windows_events import NULL
import email
from inspect import trace
from multiprocessing.sharedctypes import Value
from pickle import TRUE
from plistlib import UID
from turtle import position
from django import views
from django.forms import EmailInput
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from crowdfunding.models import Donation,  feedbacks, public_donors, topdonors, transactions,pos
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


# about page
def about_page(request):
    return render(request,'about.html')


# contact page
def contact_page(request):
    if request.method=="POST":
        fname=request.POST["fullname"]
        femail=request.POST['email']
        fmessage=request.POST['message']
        savemessage=feedbacks(fu_name=fname,fu_email=femail,fu_message=fmessage)
        savemessage.save()
        return redirect('home.html')


    return render(request,'contact.html')


# all donations
def donate_now_page(request):
    aprv_data=adata(request)

    return render(request,'donation.html',{'ad':aprv_data})

# success stories
def success_stories(request):
    s_data=Donation.objects.filter(donation_status='s')
    return render(request,'success_stories.html',{'sd':s_data})


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
        post=Donation(uid=request.user,full_name=fname,email=email,phone=mob,address=address,donation_title=title,donation_description=desc,purpose=purpose,required_amount=amount,image=image)
        post.save()
        return redirect('req-donation')



    return render(request,'req_donation.html')


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
    topdonorsdata=topdonors_data(request)
    
    return render(request,'home.html',{'sd':s_data,'ad':aprv_data,'td':topdonorsdata})

#retriving approved data   
def adata(request):
    data=Donation.objects.filter(donation_status='a')
    return(data)

#retriving donation completed data      
def sdata(request):
    data=Donation.objects.filter(donation_status='s')
    return(data)



#donation details post from donates page
def donations_details(request,slugs,id):
    data=Donation.objects.get(slugs=slugs)
    did=id
    others=Donation.objects.filter(donation_status='a').exclude(id=did)

    # get contibutors list
    get_contibutors_list=transactions.objects.filter(did=did).order_by("-amount")
    
    # pagination
    paginator=Paginator(get_contibutors_list,5)
    pg_num=request.GET.get('page')
    pg_obj=paginator.get_page(pg_num)
    
    posdata=get_pos_element(request)
    topdonorsdata=topdonors_data(request)
    # for i in range(count):




    if request.method == "POST":
        if request.user.is_authenticated==True:
            did=request.POST['donation-id']
            amount=int(request.POST['amount'])
            uuid=request.user

            # upates amount in donation model and checks status of donation
            update_donation=Donation.objects.filter(id=did).get()
            update_donation.recieved_amount=int(update_donation.recieved_amount)+int(amount)
            update_donation.if_success()
            update_donation.save()

            # update donations amount in topdonors model
            try:
                obj=topdonors.objects.filter(uid=uuid).get()
                obj.total_amount=obj.total_amount+amount
                obj.save()
            except :
                add_contribution=topdonors(uid=request.user,status='user',total_amount=amount)
                add_contribution.save()

            post_transaction=transactions(did=Donation.objects.get(id=did),uid=uuid,amount=amount)
            post_transaction.save()


        else:
            did=request.POST['donation-id']
            name=request.POST['fullname']
            phone=request.POST['phone']
            emails=request.POST['email']
            address=request.POST['address']
            amount=request.POST['amount']
            
            # upates amount in donation model and checks status of donation
            update_donation=Donation.objects.filter(id=did).get()
            update_donation.recieved_amount=int(update_donation.recieved_amount)+int(amount)
            update_donation.if_success()
            update_donation.save()

            try:
                pd_id=public_donors.objects.filter(email=emails).get()    
                try:
                    td_obj=topdonors.objects.get(pid=pd_id)
                    td_obj.total_amount=int(td_obj.total_amount)+int(amount)
                    td_obj.save()
                except:
                    add_topdonor=topdonors(pid=pd_id,total_amount=amount,status='unregistered')
                    add_topdonor.save()
                    print('added to topdonor')
            except:
                add_donor=public_donors(name=name,email=emails,address=address,phone=phone)
                add_donor.save()
                pd_id=public_donors.objects.filter(email=emails).get()    

                print(add_donor)
                try:
                    td_obj=topdonors.objects.get(pid=public_donors.objects.get(email=emails))
                    td_obj.total_amount=int(td_obj.total_amount)+int(amount)
                    td_obj.save()
                except:
                    add_topdonor=topdonors(pid=pd_id,total_amount=amount,status='unregistered')
                    add_topdonor.save()
                    print('added to topdonor')
            pd_id=public_donors.objects.filter(email=emails).get()
            add_transaction=transactions(pid=pd_id,did=Donation.objects.get(id=did),amount=amount)
            add_transaction.save()
 
            
    return render(request,'fullpost.html',{'ob':others,'inf':data,'clist':pg_obj,'td':topdonorsdata,'pos':posdata})

# get position tags and css class
def get_pos_element(request):
    get_data=pos.objects.all()
    return get_data

#get top donors list
def topdonors_data(request):
    top_donors=topdonors.objects.order_by('-total_amount')[:5]
    j=0
    for i in top_donors:
        posdata=get_pos_element(request)
        p=posdata[j]
        i.pos=p.tag
        j=j+1
    y=top_donors[0]
    print(y.pos)
    return top_donors

# profile page
def profile(request):
    user_contributions=transactions.objects.filter(uid=request.user)
    raised_donations=Donation.objects.filter(uid=request.user)
    return render(request,'profile.html',{'uc':user_contributions,'rd':raised_donations})