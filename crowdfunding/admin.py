from django.contrib import admin
from crowdfunding.models import Donation, feedbacks, public_donors, topdonors, transactions
# Register your models here.
admin.site.site_header="CROWD FUNDING"

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slugs": ("donation_title",)}
    list_display=('id','donation_title','required_amount','donation_status','progress')

class feedbacksAdmin(admin.ModelAdmin):
    list_display=('fu_name','fu_email','fu_message')

class transactionsAdmin(admin.ModelAdmin):
    list_display=('did','uid','amount','date_and_time')

class topDonorsAdmin(admin.ModelAdmin):
    list_display=('id','status','total_amount','updated')

class public_DonorAdmin(admin.ModelAdmin):
    list_display=('id','name','email')

admin.site.register(public_donors,public_DonorAdmin)
admin.site.register(feedbacks,feedbacksAdmin)
admin.site.register(transactions,transactionsAdmin)
admin.site.register(topdonors,topDonorsAdmin)
