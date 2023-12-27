# decorators.py
from django.shortcuts import HttpResponseRedirect
from .models import MonthYear, PublisherProfile

def authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/logout")
        if request.user.publisherprofile.status == "Pending":
            return HttpResponseRedirect("/sign-up-suc")
        return view_func(request, *args, **kwargs)

    return wrapper

def authentication_required_pending(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/logout")
        if request.user.publisherprofile.status == "Active":
            return HttpResponseRedirect("/logout")
        if request.user.phone == "":
            return HttpResponseRedirect("/logout")
        return view_func(request, *args, **kwargs)

    return wrapper

def admin_privilege(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.publisherprofile.privilege == "1":
            return HttpResponseRedirect("/logout")
        return view_func(request, *args, **kwargs)

    return wrapper

def check_month_year(view_func):
    def wrapper(request, *args, **kwargs):
        rows = MonthYear.objects.filter().count()
        if rows == 0:
            return HttpResponseRedirect("/publishers/all-active-publishers")
        return view_func(request, *args, **kwargs)
    return wrapper

def publisher_profile_privilege(view_func):  # Add any additional parameters you need
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username')
        profile = PublisherProfile.objects.get(username=username)
        if not request.user.publisherprofile.privilege == "1" and profile.parent_id != request.user.publisherprofile.username:
            return HttpResponseRedirect("/publishers/all-active-publishers")
        return view_func(request, *args, **kwargs)
    return wrapper

def restrict_followers(view_func):  # Add any additional parameters you need
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username')
        profile = PublisherProfile.objects.get(username=username)
        if profile.parent_id != profile.username:
            return HttpResponseRedirect("/publishers/all-active-publishers")
        return view_func(request, *args, **kwargs)
    return wrapper
    