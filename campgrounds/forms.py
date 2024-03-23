from django.forms import DateInput, ModelForm
from django import forms
from .models import Campgrounds, Reviews,Booking,Availability 
from django.contrib.auth.models import User
from django.core.validators import EmailValidator 
from django.core.exceptions import ValidationError

class CampgroundForm(forms.ModelForm):
    class Meta:
        model = Campgrounds
        exclude = ['user','average_rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'total_camps': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Camps'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Start Date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'End Date'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
    def clean_total_camps(self):
        total_camps = self.cleaned_data.get('total_camps')
        if total_camps < 5:
            raise ValidationError("The minimum number of camps must be 5.")
        return total_camps


class SignUpForm(ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label=''
    )

class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        exclude = ['campground_id','user']
        widgets = {
            'text_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your review here'}),
            'rating': forms.Select(attrs={'class': 'form-control'})  # Style the rating field as a select dropdown
        }
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['campground_id', 'f_cancel', 'f_confirmed', 'user']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Start Date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'End Date'}),
            'nb_persons': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Persons'}),
        }
    def clean_nb_persons(self):
        nb_persons = self.cleaned_data.get('nb_persons')
        if nb_persons < 1:
            raise forms.ValidationError("Number of persons must be at least 1.")
        return nb_persons


class AvailabilityForm(ModelForm):
    class Meta:
        model = Availability
        exclude = '__all__'