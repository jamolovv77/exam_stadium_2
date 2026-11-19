from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import *


def home(request):
    if request.user.is_authenticated:
        return redirect('fields')
    return redirect('login')


def registration(request):
    if request.method == 'POST':
        data = request.POST
        if CustomUser.objects.filter(username=data['username']).exists():
            messages.error(request, "This username already exists")
            return redirect('registration')

        user = CustomUser.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        # photo is optional
        if request.FILES.get('photo'):
            user.photo = request.FILES['photo']
            user.save()
        return redirect('login')
    return render(request, 'auth.html', {"page": "registration"})


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('fields')
        messages.error(request, "Wrong username or password")
        return redirect('login')
    return render(request, 'auth.html', {"page": "login"})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def get_fields(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    fields = Field.objects.all()
    categories = Category.objects.all()

    if query:
        fields = fields.filter(Q(name__icontains=query) | Q(address__icontains=query))

    if category_id:
        fields = fields.filter(category_id=category_id)

    return render(request, 'fields.html', {
        "fields": fields,
        "categories": categories,
        "query": query,
        "category_id": category_id
    })


@login_required
def book_field(request, pk):
    field = get_object_or_404(Field, pk=pk)

    if request.method != 'POST':
        return redirect('fields')

    # server check: a busy field cannot be booked
    if not field.is_free:
        messages.error(request, "This field is busy")
        return redirect('fields')

    data = request.POST
    has_team = data.get('has_team') == 'yes'
    players_needed = None

    if not has_team:
        value = data.get('players_needed', '')
        if not value.isdigit() or int(value) < 1:
            messages.error(request, "Enter how many players you need")
            return redirect('fields')
        players_needed = int(value)

    Booking.objects.create(
        user=request.user,
        field=field,
        has_team=has_team,
        players_needed=players_needed
    )
    field.is_free = False
    field.save()
    messages.success(request, "Field booked")
    return redirect('my_fields')


@login_required
def my_fields(request):
    # my active bookings
    bookings = Booking.objects.filter(user=request.user, status='active')
    bookings = bookings.select_related('field')
    bookings = bookings.prefetch_related('participants__user')

    # history: everything except active
    history = Booking.objects.filter(user=request.user)
    history = history.exclude(status='active')
    history = history.select_related('field')

    return render(request, 'bookings.html', {"bookings": bookings, "history": history})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user, status='active')
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        booking.field.is_free = True
        booking.field.save()
        messages.success(request, "Booking cancelled")
    return redirect('my_fields')


@login_required
def finish_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user, status='active')
    if request.method == 'POST':
        booking.status = 'completed'
        booking.save()
        booking.field.is_free = True
        booking.field.save()
        messages.success(request, "Game finished")
    return redirect('my_fields')


@login_required
def play_together(request):
    # active bookings that are looking for players
    bookings = Booking.objects.filter(status='active', has_team=False)
    bookings = bookings.select_related('field', 'user')
    bookings = bookings.prefetch_related('participants__user')
    bookings = bookings.annotate(joined_count=Count('participants'))

    return render(request, 'play_together.html', {"bookings": bookings})


@login_required
def join_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, status='active', has_team=False)
    if request.method == 'POST':
        if booking.user == request.user:
            messages.error(request, "You cannot join your own booking")
        elif Participant.objects.filter(booking=booking, user=request.user).exists():
            messages.error(request, "You already joined")
        elif booking.participants.count() >= booking.players_needed:
            messages.error(request, "The team is full")
        else:
            Participant.objects.create(booking=booking, user=request.user)
            messages.success(request, "You joined the team")
    return redirect('play_together')


@login_required
def leave_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        Participant.objects.filter(booking=booking, user=request.user).delete()
        messages.success(request, "You left the team")
    return redirect('play_together')


@login_required
def profile(request):
    return render(request, 'profile.html', {
        "profile_user": request.user,
        "bookings_count": request.user.bookings.count()
    })


@login_required
def user_profile(request, pk):
    profile_user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'profile.html', {
        "profile_user": profile_user,
        "bookings_count": profile_user.bookings.count()
    })


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        data = request.POST

        # username must be unique
        if CustomUser.objects.filter(username=data['username']).exclude(pk=user.pk).exists():
            messages.error(request, "This username is already taken")
            return redirect('profile')

        user.username = data['username']
        user.email = data['email']
        user.phone = data['phone']
        user.about = data['about']
        if request.FILES.get('photo'):
            user.photo = request.FILES['photo']
        user.save()
        messages.success(request, "Profile updated")
    return redirect('profile')




@login_required
def booking_detail(request, pk):
    # only my own booking, someone else's booking gives 404
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'booking_detail.html', {"booking": booking})