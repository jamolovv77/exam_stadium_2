from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import *





def home(request):
    if request.user.is_authenticated:
        return redirect('fields')
    return redirect ('login')






def registration(request):
    if request.method =='POST':
        data =request.POST
        if CustomUser.objects.filter(username=data['username']).exists():
            return redirect('registration')
        user =CustomUser.objects.create_user(
            username=data['username'],
            email= data['email'],
            password=data['password'],
        )





        if request.FILES.get('photo'):
            user.photo =request.FILES['photo']
            user.save()
        return redirect('login')
    return render(request, 'auth.html',{"page":"registration"})








def login_user(request):
    if request.method =='POST':
        data =request.POST
        user =authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('fields')
        return redirect('login')
    return render(request,'auth.html',{"page":"login"})






@login_required
def logout_user(request):
    logout(request)
    return redirect('login')







@login_required
def giriftani_igrok(request):
    query =request.GET.get('q')
    category_id =request.GET.get('category')
    fields =Field.objects.all()
    categories =Category.objects.all()


    if query:
        fields = fields.filter(Q(name__icontains=query) or Q(address__icontains=query))

    if category_id:
        fields = fields.filter(category_id=category_id)





    return render(request,'fields.html', {
    "fields": fields,
    "categories": categories,
    "query": query,
    "category_id":category_id,
    })







@login_required
def book_igrok(request, pk):
    field =get_object_or_404(Field, pk=pk)








    data = request.POST
    has_team = data.get('has_team') =='yes'
    players_needed =None
    if not has_team:
        value = data.get('players_needed', '')
        if not value.isdigit() or int(value) <=1:
            messages.error(request, "chand bozingar wumo lozim dored")
            return redirect('fields')
        

    Booking.objects.create(
        user=request.user,
        field=field,
        has_team=has_team,
        players_needed=players_needed
    )
    field.is_free = False
    field.save()
    messages.success(request, "polya band ast")
    return redirect('my_fields')





@login_required
def igroko_ma(request):

    bookings =Booking.objects.filter(user=request.user, status='active')
    bookings =bookings.prefetch_related('participants__user')





    history =Booking.objects.filter(user=request.user)
    history =history.exclude(status='active')

    return render(request, 'bookings.html',{"bookings":bookings, "history":history})





@login_required
def atmenai_zakaho(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user, status='active')
    if request.method == 'POST':
        booking.status = 'atmena'
        booking.save()
        messages.success(request, " polya atmena wud")
    return redirect('my_fields')





@login_required
def tamomkardani_kor(request,pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user, status='active')
    if request.method =='POST':
        booking.status = 'kabul karda wud'
        booking.save()
        booking.field.is_free = True
        booking.field.save()
        messages.success(request, "bozi bud wud")
    return redirect('my_fields')




@login_required
def play_katidigaro(request):
    bookings =Booking.objects.filter(status='active', has_team=False)
    bookings =bookings.select_related('field', 'user')
    bookings =bookings.prefetch_related('participants__user')
    
    return render(request, 'play_together.html', {"bookings": bookings})







@login_required
def baromad_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        Participant.objects.filter(booking=booking, user=request.user).delete()
        messages.success(request, "wmo baromaded az bozi")
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
def profil(request):
    user = request.user
    if request.method == 'POST':
        data = request.POST
        if CustomUser.objects.filter(username=data['username']).exists():
            return redirect('profile')
        user.username = data['username']
        user.email =data['email']
        user.phone =data['phone']
        user.about =data['about']
        if request.FILES.get('photo'):
            user.photo = request.FILES['photo']
        user.save()
    return redirect('profile')



@login_required
def booking_detalho(request, pk):
    booking =get_object_or_404(Booking, pk=pk,user=request.user)
    return render(request, 'booking_detail.html',{"booking":booking})