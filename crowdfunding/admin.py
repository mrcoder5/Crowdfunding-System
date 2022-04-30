from django.contrib import admin
from crowdfunding.models import Donation, feedbacks, topdonors, transactions
# Register your models here.
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slugs": ("donation_title",)}
    list_display=('id','donation_title','required_amount','donation_status','progress')

class feedbacksAdmin(admin.ModelAdmin):
    list_display=('fu_name','fu_email','fu_message')

class transactionsAdmin(admin.ModelAdmin):
    list_display=('did','uid','amount','date_and_time')

class topDonorsAdmin(admin.ModelAdmin):
    list_display=('did','uid','total_amount','updated')


admin.site.register(feedbacks,feedbacksAdmin)
admin.site.register(transactions,transactionsAdmin)
admin.site.register(topdonors,topDonorsAdmin)
