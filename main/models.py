from tokenize import group
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.


# phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$", "The phone number provided is invalid")
#  validators=[phone_validator], unique=True

class User(AbstractUser):
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)

    REQUIRED_FIELDS = ["phone"]

class PublisherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, blank=True)
    DOB = models.CharField(max_length=100, blank=True)
    parent_id = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=150,blank=True)
    email = models.EmailField(max_length=150,blank=True)
    groupName = models.CharField(max_length=150,blank=True)
    pioneer = models.CharField(max_length=150, blank=True)
    appointment = models.CharField(max_length=150, blank=True)
    privilege = models.CharField(max_length=150,blank=True)
    pic = models.CharField(max_length=150,blank=True)
    status = models.CharField(max_length=150,blank=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        PublisherProfile.objects.create(user=instance)
    instance.publisherprofile.save()


class MonthYear(models.Model):
    # todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    month = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=100, blank=True)
    current = models.BooleanField()
    open = models.BooleanField()

    def __str__(self):
        return self.month 


class PublisherReport(models.Model):
    publisher_username = models.CharField(max_length=150, blank=True)
    group = models.CharField(max_length=150, blank=True)
    pioneer = models.CharField(max_length=150, blank=True)
    appointment = models.CharField(max_length=150, blank=True)
    month = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=100, blank=True)
    month_year_id = models.CharField(max_length=150, blank=True)
    placements = models.IntegerField(blank=True)
    video_showings = models.IntegerField(blank=True)
    hours = models.IntegerField(blank=True)
    return_visits = models.IntegerField(blank=True)
    bible_studies = models.IntegerField(blank=True)
    comments = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.month_year_id 