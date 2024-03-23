from datetime import timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from .models import Campgrounds,Reviews, Booking, Availability
from .forms import SignUpForm, LoginForm, CampgroundForm, ReviewForm, BookingForm, AvailabilityForm
from django.contrib import messages
import json
from django.db.models import Avg

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                             email=form.cleaned_data['email'],
                                             password=form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)
            return redirect('campgrounds')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            if '@' in username_or_email:
                kwargs = {'email': username_or_email}
            else:
                kwargs = {'username': username_or_email}

            user = authenticate(request, **kwargs, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome Back! You have successfully logged in.")
                return redirect('home') 
            else:
                messages.error(request, "Invalid username/email or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')

def campgrounds(request):
    query = request.GET.get('search', '')  
    owner_filter = request.GET.get('owner')
    rating_sort = request.GET.get('rating')
    price_sort = request.GET.get('price')

    campgrounds = Campgrounds.objects.all()

    if query:
        campgrounds = campgrounds.filter(title__istartswith=query)

    if owner_filter:
        campgrounds = campgrounds.filter(user__username=owner_filter)

    if rating_sort:
        if rating_sort == 'low_to_high':
            campgrounds = campgrounds.order_by('average_rating')
        elif rating_sort == 'high_to_low':
            campgrounds = campgrounds.order_by('-average_rating')

    if price_sort:
        if price_sort == 'low_to_high':
            campgrounds = campgrounds.order_by('price')
        elif price_sort == 'high_to_low':
            campgrounds = campgrounds.order_by('-price')

    owners = User.objects.filter(campgrounds__in=campgrounds).values_list('username', flat=True).distinct()

    return render(request, 'campgrounds.html', {'campgrounds': campgrounds, 'owners': owners})

def show_campground(request, camp_id):
    campground = Campgrounds.objects.get(id=camp_id)
    reviews = Reviews.objects.filter(campground_id=camp_id).exclude(rating='NR')
    available = Availability.objects.all()
    return render(request, 'campground.html', {'camp': campground, 'reviews': reviews, 'available': available})

def add_campground(request):
    form = CampgroundForm()
    if request.user.is_authenticated == False:
        messages.error(request, "You must be signed in to perform such action!")
        return HttpResponseForbidden("You are not authorized to add a campground.")
    if request.method == 'POST':
        form = CampgroundForm(request.POST, request.FILES)
        if form.is_valid():
            campground = form.save(commit=False)
            campground.user = request.user
            if campground.end_date <= campground.start_date:
                messages.error(request, "End date must be after the start date.")
                return render(request, 'addCampground.html', {'form': form})
            if campground.total_camps < 5:
                messages.error(request, "Number of available camps must be at least 5.")
                return render(request, 'addCampground.html', {'form': form})
            campground.save()

            num_days = (campground.end_date - campground.start_date).days + 1

            for i in range(num_days):
                date = campground.start_date + timedelta(days=i)
                availability = Availability(campground_id=campground, date=date, num_camps_available=campground.total_camps)
                availability.save()
            messages.success(request, "You have successfully added a new campground!")
            return redirect('campgrounds')
    return render(request, 'addCampground.html', {'form': form})

def edit_campground(request, camp_id):
    camp = Campgrounds.objects.get(id=camp_id)
    if camp.user != request.user:
        messages.error(request, "You must be signed in to perform such action!")
        return HttpResponseForbidden("You are not authorized to edit this campground.")
    if request.method == 'POST':
        form = CampgroundForm(request.POST, request.FILES, instance=camp)
        if form.is_valid():
            if form.cleaned_data['end_date'] <= form.cleaned_data['start_date']:
                messages.error(request, "End date must be after the start date.")
                return render(request, 'editCampground.html', {'form': form})
            if form.cleaned_data['total_camps'] < 5:
                messages.error(request, "Number of available camps must be at least 5.")
                return render(request, 'editCampground.html', {'form': form})
            form.save()
            message = f"You have successfully edited {camp.title} campground!"
            messages.success(request, message)
            return redirect('campgrounds')
    else:
        form = CampgroundForm(instance=camp)
    return render(request, 'editCampground.html', {'form': form})

def delete_campground(request,camp_id):
    camp = Campgrounds.objects.get(id=camp_id)
    camp.delete()
    message = f"You have successfully deleted {camp.title} campground!"
    messages.success(request, message)
    return redirect(campgrounds)
       
def add_review(request, camp_id):
    campground = get_object_or_404(Campgrounds, id=camp_id)
    if not request.user.is_authenticated:
        messages.error(request, "You must be signed in to perform such action!")
        return HttpResponseForbidden("You are not authorized to add a review.")
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.campground_id = campground
            review.user = request.user  
            review.save()

            # Recalculate average rating for the campground
            reviews = Reviews.objects.filter(campground_id=camp_id).exclude(rating='NR')
            total_rating = sum(int(review.rating) for review in reviews)
            avg_rating = total_rating / len(reviews) if len(reviews) > 0 else 0
            campground.average_rating = avg_rating
            campground.save()
            messages.success(request, "You have succesfully added a review!")
            return redirect('showCampground', camp_id=camp_id)
    return render(request, 'addReview.html', {'form': form})

def edit_review(request, camp_id, review_id):
    review = Reviews.objects.get(id=review_id)
    if review.user != request.user:
        messages.error(request, "You must be signed in to perform such action!")
        return HttpResponseForbidden("You are not authorized to edit this review.")
    form = ReviewForm(instance=review)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()

            # Recalculate average rating for the campground
            reviews = Reviews.objects.filter(campground_id=camp_id).exclude(rating='0')
            total_rating = sum(int(review.rating) for review in reviews)
            avg_rating = total_rating / len(reviews)
            campground = Campgrounds.objects.get(id=camp_id)
            campground.average_rating = avg_rating
            campground.save()
            messages.success(request, "You have succesfully edited this review!")
            return redirect('showCampground', camp_id=camp_id)
    return render(request, 'editReview.html', {'form': form})

def delete_review(request,camp_id,review_id):
    review = Reviews.objects.get(id=review_id)
    review.delete()
    messages.success(request, "You have succesfully deleted this review!")
    return redirect('showCampground',camp_id=camp_id)
       
def booked_campgrounds(request):
    booked_camps = Booking.objects.all()
    if request.user.is_authenticated==False:
        messages.error(request, "You must be signed in to perform such action!")
        return HttpResponseForbidden("You are not authorized to view the booked campgrounds.")
    return render(request,'bookedCampgrounds.html',{'booked_camps':booked_camps})     


def book_campground(request, camp_id):
    campground = Campgrounds.objects.get(id=camp_id)
    
    if not request.user.is_authenticated:
        messages.error(request, "You must be signed in to perform such action!")
        return HttpResponseForbidden("You are not authorized to book a campground.")

    available_dates = Availability.objects.filter(campground_id=campground, num_camps_available__gt=0).values_list('date', flat=True)
    available_dates = [d.isoformat() for d in available_dates]

    bookingForm = BookingForm(request.POST or None)

    if request.method == 'POST' and bookingForm.is_valid():
        booking = bookingForm.save(commit=False)
        booking.user = request.user
        booking.campground_id = campground 
        booking.f_cancel = False
        
        start_date = booking.start_date
        end_date = booking.end_date
        current_date = start_date
        while current_date <= end_date:
            availability = Availability.objects.get(campground_id=campground, date=current_date)
            available_camps = availability.num_camps_available
            booked_camps = booking.nb_persons
            
            if booked_camps > available_camps:
                return HttpResponseForbidden("Not enough camps available for the specified date: {}".format(current_date))
            
            current_date += timedelta(days=1)
        
        current_date = start_date
        while current_date <= end_date:
            availability = Availability.objects.get(campground_id=campground, date=current_date)
            available_camps = availability.num_camps_available
            booked_camps = booking.nb_persons
            
            availability.num_camps_available -= booked_camps
            availability.save()
            
            current_date += timedelta(days=1)
        
        booking.save()
        message = f"You have succesfully booked {campground.title} campground!"
        messages.success(request, message)
        return redirect('campgrounds')
    
    return render(request, 'bookCampground.html', {'form': bookingForm, 'camp_id': camp_id, 'available_dates': json.dumps(available_dates)})