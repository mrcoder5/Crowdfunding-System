from django.contrib import admin
from crowdfunding.models import Donation, feedbacks, public_donors, topdonors, transactions,pos
# Register your models here.
admin.site.site_header="CROWD FUNDING"


class DonationAdmin(admin.ModelAdmin):
    list_display=('id','donation_title','required_amount','donation_status','progress')
    prepopulated_fields = {'slugs': ('donation_title',)}

class feedbacksAdmin(admin.ModelAdmin):
    list_display=('fu_name','fu_email','fu_message')

class transactionsAdmin(admin.ModelAdmin):
    list_display=('did','uid','pid','amount','date_and_time')

class topDonorsAdmin(admin.ModelAdmin):
    list_display=('id','status','total_amount','updated')

class public_DonorAdmin(admin.ModelAdmin):
    list_display=('id','name','email')

class posAdmin(admin.ModelAdmin):
    list_display=('id','tag')

admin.site.register(pos,posAdmin)
admin.site.register(public_donors,public_DonorAdmin)
admin.site.register(feedbacks,feedbacksAdmin)
admin.site.register(transactions,transactionsAdmin)
admin.site.register(topdonors,topDonorsAdmin)
admin.site.register(Donation,DonationAdmin)