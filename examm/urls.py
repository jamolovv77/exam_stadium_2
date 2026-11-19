from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', registration, name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('fields/', get_fields, name='fields'),
    path('fields/<int:pk>/book/', book_field, name='book_field'),
    path('my-fields/', my_fields, name='my_fields'),
    path('bookings/<int:pk>/cancel/', cancel_booking, name='cancel_booking'),
    path('bookings/<int:pk>/finish/', finish_booking, name='finish_booking'),
    path('play-together/', play_together, name='play_together'),
    path('bookings/<int:pk>/join/', join_booking, name='join_booking'),
    path('bookings/<int:pk>/leave/', leave_booking, name='leave_booking'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('users/<int:pk>/', user_profile, name='user_profile'),
        path('bookings/<int:pk>/', booking_detail, name='booking_detail'),
]