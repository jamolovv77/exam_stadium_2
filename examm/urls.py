from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', registration, name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('fields/', giriftani_igrok, name='fields'),
    path('fields/<int:pk>/book/', book_igrok, name='book_field'),
    path('my-fields/', igroko_ma, name='my_fields'),
    path('bookings/<int:pk>/cancel/', atmenai_zakaho, name='cancel_booking'),
    path('bookings/<int:pk>/finish/', tamomkardani_kor, name='finish_booking'),
    path('play-together/', play_katidigaro, name='play_together'),
    path('bookings/<int:pk>/leave/', baromad_booking, name='leave_booking'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profil, name='profile_edit'),
    path('users/<int:pk>/', user_profile, name='user_profile'),
    path('bookings/<int:pk>/', booking_detalho, name='booking_detail'),
]