from django import template
import uuid
from calendar import month
from cmath import nan
from multiprocessing import cpu_count
from queue import Empty
# from tkinter.messagebox import YES
# from tkinter.tix import Tree
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate
from ..forms import SignUpForm, AddFollowerForm, AddMonthYearForm
from django.shortcuts import render, redirect
from ..models import PublisherProfile, User, MonthYear, PublisherReport
from django.utils.crypto import get_random_string
import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.models import Avg
import csv
from django.views import View
# pip install xlwt first
import xlwt

import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.reader.excel import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Font

import csv
from io import TextIOWrapper
import xlrd
from django.contrib import messages

from ..decorators import authentication_required_pending


User = get_user_model()


register = template.Library()


# Create your views here.
def index(response):
    if response.user.is_authenticated == True:
        return HttpResponseRedirect("/logout")

    return render(response, "main/index.html", {})


def signup_view(request):

    if request.user.is_authenticated == True:
        return HttpResponseRedirect("/logout")

    form = SignUpForm(request.POST)
    if form.is_valid():
        query_phone = PublisherProfile.objects.filter(
            phone=form.cleaned_data.get('phone')).count()
        if len(form.cleaned_data.get('first_name')) > 0 and len(form.cleaned_data.get('last_name')) > 0 and len(form.cleaned_data.get('gender')) > 0 and len(form.cleaned_data.get('phone')) == 11 and form.cleaned_data.get('phone').isdigit() and query_phone == 0 and form.cleaned_data.get('phone') == form.cleaned_data.get('phone2') and len(form.cleaned_data.get('password1')) > 0 and form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
            user = form.save()
            user.refresh_from_db()
            user.publisherprofile.first_name = form.cleaned_data.get(
                'first_name')
            user.publisherprofile.middle_name = form.cleaned_data.get(
                'middle_name')
            user.publisherprofile.last_name = form.cleaned_data.get(
                'last_name')
            user.publisherprofile.username = form.cleaned_data.get(
                'first_name') + form.cleaned_data.get('username')
            user.publisherprofile.gender = form.cleaned_data.get('gender')
            user.publisherprofile.email = form.cleaned_data.get('email')
            user.publisherprofile.phone = form.cleaned_data.get('phone')
            user.publisherprofile.pioneer = 0
            user.publisherprofile.appointment = 0
            user.publisherprofile.parent_id = form.cleaned_data.get(
                'first_name') + form.cleaned_data.get('username')
            user.publisherprofile.status = 'Pending'
            user.publisherprofile.privilege = 0
            user.publisherprofile.groupName = 0
            user.publisherprofile.created_at = datetime.datetime.now()
            user.save()
            username = form.cleaned_data.get('username')
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=phone, password=password)
            login(request, user)
            return HttpResponseRedirect("/sign-up-suc")
        else:
            return HttpResponseRedirect("/sign-up")
    else:
        form = SignUpForm()
    return render(request, 'main/sign-up.html', {'form': form})



@authentication_required_pending
def sign_up_suc(response):
    publisher = response.user

    form = AddFollowerForm(response.POST)
    if form.is_valid():
        phone_value = form.cleaned_data.get('phone')
        query_phone = PublisherProfile.objects.filter(phone=phone_value).exclude(
            parent_id=publisher.publisherprofile.username).count()
        if len(form.cleaned_data.get('first_name')) > 0 and len(form.cleaned_data.get('last_name')) > 0 and len(form.cleaned_data.get('gender')) > 0 and len(form.cleaned_data.get('phone')) == 11 or len(form.cleaned_data.get('phone')) == 0 or form.cleaned_data.get('phone').isdigit() and query_phone == 0:

            if len(form.cleaned_data.get('phone')) == 0:
                phonex = publisher.publisherprofile.phone
            else:
                phonex = phone_value

            user = form.save()
            user.refresh_from_db()
            user.publisherprofile.first_name = form.cleaned_data.get(
                'first_name')
            user.publisherprofile.middle_name = form.cleaned_data.get(
                'middle_name')
            user.publisherprofile.last_name = form.cleaned_data.get(
                'last_name')
            user.publisherprofile.username = form.cleaned_data.get(
                'first_name') + form.cleaned_data.get('username')
            user.publisherprofile.gender = form.cleaned_data.get('gender')
            user.publisherprofile.phone = phonex
            user.publisherprofile.pioneer = 0
            user.publisherprofile.appointment = 0
            user.publisherprofile.privilege = 0
            user.publisherprofile.parent_id = publisher.publisherprofile.username
            user.publisherprofile.status = 'Pending'
            user.publisherprofile.created_at = datetime.datetime.now()
            user.save()
            User.objects.filter(username=form.cleaned_data.get(
                'username')).update(phone="", password="")
            # username = form.cleaned_data.get('first_name') + form.cleaned_data.get('username')

            # username = form.cleaned_data.get('first_name') + form.cleaned_data.get('username') + get_random_string(length=6)
            # password = form.cleaned_data.get('password1')

            # user = authenticate(username=username, password=password)
            # login(response, user)
            # return HttpResponseRedirect("/sign-up-suc-redirect")
            form = AddFollowerForm()
            return redirect("/sign-up-suc")
        else:
            return redirect("/sign-up-suc")

    else:
        form = AddFollowerForm()

    followers = PublisherProfile.objects.filter(parent_id=publisher.publisherprofile.username).exclude(
        user_id=publisher.publisherprofile.user_id)
    # followers = PublisherProfile.objects.all()

    # update_follower_form = UpdateFollowerForm(response.POST)
    # if update_follower_form.is_valid():
    #     t = PublisherProfile.objects.get(id=1)

    # username2 = User.objects.all()
    return render(response, "main/sign-up-suc.html", {"publisher": publisher, "followers": followers, 'form': form})


@authentication_required_pending
def update_acct_pending_details(request):
    publisher = request.user
   
    if request.method == 'POST':

        userID = request.POST.get('userID')
        publisherModel = PublisherProfile.objects.get(user_id=userID)
        userModel = User.objects.get(id=userID)

        if request.POST.get("update_pen_details_submitButton"):
            phone_value = request.POST.get("phone")
            if len(phone_value) == 0:
                phonex = publisher.publisherprofile.phone
            else:
                phonex = phone_value

            query_phone = PublisherProfile.objects.filter(phone=phone_value).exclude(
                parent_id=publisher.publisherprofile.username).count()
            if len(request.POST.get("fname")) > 0 and len(request.POST.get("surname")) > 0 and len(request.POST.get("gender")) > 0 and len(request.POST.get("phone")) == 11 and request.POST.get("phone").isdigit() and query_phone == 0 and request.POST.get("phone") == request.POST.get("phone2"):
                publisherModel.first_name = request.POST.get("fname")
                publisherModel.middle_name = request.POST.get("mname")
                publisherModel.last_name = request.POST.get("surname")
                publisherModel.gender = request.POST.get("gender")
                publisherModel.email = request.POST.get("email")
                publisherModel.phone = phonex
                publisherModel.updated_at = datetime.datetime.now()
                # publisherModel.status = "Active"
                # publisherModel.groupName = 1
                # publisherModel.pioneer = 1
                # publisherModel.appointment = 1
                # publisherModel.privilege = 1
                publisherModel.save()

                userModel.first_name = request.POST.get("fname")
                userModel.last_name = request.POST.get("surname")
                userModel.email = request.POST.get("email")
                userModel.phone = phonex
                userModel.save()

            return redirect("/sign-up-suc/acct-pen-details/")

        elif request.POST.get("edit-follower-button"):
            phone_value = request.POST.get("secondary_phone")
            if len(phone_value) == 0:
                phonex = publisher.publisherprofile.phone
            else:
                phonex = phone_value

            query_phone = PublisherProfile.objects.filter(phone=phone_value).exclude(
                parent_id=publisher.publisherprofile.username).count()
            if len(request.POST.get("fname")) > 0 and len(request.POST.get("surname")) > 0 and len(request.POST.get("gender")) > 0 and len(request.POST.get("secondary_phone")) == 11 or len(request.POST.get("secondary_phone")) == 0 or request.POST.get("secondary_phone").isdigit() and query_phone == 0:
                publisherModel.first_name = request.POST.get("fname")
                publisherModel.middle_name = request.POST.get("mname")
                publisherModel.last_name = request.POST.get("surname")
                publisherModel.gender = request.POST.get("gender")
                publisherModel.phone = phonex
                publisherModel.updated_at = datetime.datetime.now()
                publisherModel.save()

                userModel.first_name = request.POST.get("fname")
                userModel.last_name = request.POST.get("surname")
                userModel.phone = ""
                userModel.save()

            return redirect("/sign-up-suc")

        elif request.POST.get("acct_pen_change_password_button"):

            if len(request.POST.get('password1')) > 0 and request.POST.get('password1') == request.POST.get('password2'):

                userModel.password = make_password(
                    request.POST.get("password1"))
                userModel.save()
                update_session_auth_hash(request, request.user)
                # publisher.is_authenticated
                # userModel = authenticate(username=userModel.phone, password=userModel.password)
                # login(request, userModel)

                publisherModel.updated_at = datetime.datetime.now()
                publisherModel.save()

            return redirect("/sign-up-suc/acct-pen-details/")
    else:
        return redirect("/sign-up-suc")


def check_follower_phone_exist(request):
    publisher = request.user

    if request.method == 'POST':
        phone = request.POST.get('phone')
        if request.POST.get('phone_check_sign_up'):
            if len(phone) > 0:
                query_phone = PublisherProfile.objects.filter(phone=phone)
                if(phone.isdigit()):
                    if query_phone.exists():
                        return HttpResponse("taken")
                    else:
                        return HttpResponse("not_taken")
                else:
                    return HttpResponse("not_number")
            else:
                return HttpResponse(0)
        else:
            if len(phone) > 0:
                query_phone = PublisherProfile.objects.filter(phone=phone).exclude(
                    parent_id=publisher.publisherprofile.username)
                if(phone.isdigit()):
                    if query_phone.exists():
                        return HttpResponse("taken")
                    else:
                        return HttpResponse("not_taken")
                else:
                    return HttpResponse("not_number")

            else:
                return HttpResponse(0)
    else:
        return redirect("/sign-up-suc")

# @authentication_required_pending
def delete_follower(request):
    publisher = request.user

    if request.method == 'POST':
        id = request.POST.get('id')

        PublisherProfile.objects.get(user_id=id).delete()
        User.objects.get(id=id).delete()

        if len(id) == 0:
            return HttpResponse(0)
        else:
            return HttpResponse(1)
    else:
        return redirect("/sign-up-suc")

@authentication_required_pending
def acct_pen_details(response):
    publisher = response.user
    
    return render(response, "main/acct-pen-details.html", {"publisher": publisher})

def sign_up_suc_redirect(response):
    return redirect("/sign-up-suc")

def custom_404(request, exception):
    referring_url = request.META.get('HTTP_REFERER', None)
    return render(request, 'main/custom_404.html', {'error_message': str(exception), "referring_url":referring_url}, status=404)
