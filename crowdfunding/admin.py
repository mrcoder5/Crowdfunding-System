from django.contrib import admin
from crowdfunding.models import Donation, feedbacks
# Register your models here.
class DonationAdmin(admin.ModelAdmin):
    list_display=('id','donation_title','required_amount','donation_status')



class feedbacksAdmin(admin.ModelAdmin):
    list_display=('fu_name','fu_email','fu_message')

class supporters(admin.ModelAdmin):
    list_display=('user_name','user_age')
admin.site.register(Donation,DonationAdmin)

admin.site.register(feedbacks,feedbacksAdmin)