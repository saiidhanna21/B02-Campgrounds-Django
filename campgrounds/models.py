from django.db import models
from django.contrib.auth.models import User

RATING_CHOICES = [
    ('1', '1 ⭐'),
    ('2', '2 ⭐⭐'),
    ('3', '3 ⭐⭐⭐'),
    ('4', '4 ⭐⭐⭐⭐'),
    ('5', '5 ⭐⭐⭐⭐⭐'),
]
class Campgrounds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    total_camps = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    average_rating = models.FloatField(default=0)  # New field for storing average rating
    
    def __str__(self):
        return self.title

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    campground_id = models.ForeignKey('Campgrounds', on_delete=models.CASCADE)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='0')  # Change default value to '0'
    text_description = models.TextField()

    def __str__(self):
        return f"{self.rating} - {self.text_description}"

class Availability(models.Model):
    date = models.DateField()
    campground_id = models.ForeignKey(Campgrounds,on_delete=models.CASCADE)
    num_camps_available = models.IntegerField()
    
    def __str__(self):
        return self.num_camps_available
    
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    campground_id = models.ForeignKey(Campgrounds,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    nb_persons = models.IntegerField()
    f_cancel = models.BooleanField()
    f_confirmed = models.BooleanField()
    
    def __str__(self):
        return self.nb_persons