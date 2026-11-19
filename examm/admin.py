from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')

    # when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('photo', 'phone', 'about')}),
    )

    # when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('email', 'photo', 'phone', 'about')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'players_count')
    search_fields = ('name',)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_free')
    list_filter = ('category', 'is_free')
    search_fields = ('name', 'address')
    # hide the "Is free" checkbox: the site changes it automatically
    exclude = ('is_free',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'status', 'created_at')
    list_filter = ('status', 'has_team')
    search_fields = ('user__username', 'field__name')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'joined_at')
    list_filter = ('joined_at',)
    search_fields = ('user__username',)