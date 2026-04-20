from django.db import models
from django.contrib.auth.models import User

# -------------------------
# User Profile
# -------------------------
from django.db import models
from django.contrib.auth.models import User

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    income = models.IntegerField()
    family_size = models.IntegerField()
    car_type = models.CharField(max_length=50)  # e.g., SUV, Sports
    emi_required = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    usage = models.CharField(max_length=50)  # long drive or city

    def __str__(self):
        return self.user.username

# Car Model
class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    mileage = models.FloatField()
    seating = models.IntegerField()
    car_type = models.CharField(max_length=50)
    image = models.URLField()  # store image link

    def __str__(self):
        return self.name