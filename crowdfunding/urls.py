
from django.urls import path
from . import views

urlpatterns = [
    path('about',views.about_page, name='about'),
    path('contact',views.contact_page,name='contact'),
    path('donates',views.donate_now_page, name='donates'),
    path('full-donation',views.donation_post_page),
    path('',views.home_page),
    path('home',views.home_page, name='home'),
    path('req-donation',views.req_donation_page, name='req-donation'),
    path('login',views.login_form,name='login'),
    path('register',views.register_user,name='register'),
    path('success-stories',views.success_stories,name="success-stories"),
    path('logout',views.logout_user,name='logout'),
    path('donation/<int:id>/',views.donations_details,name='fullpost'),
]