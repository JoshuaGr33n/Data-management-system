from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..decorators import authentication_required, admin_privilege

from ..forms import AddMonthYearForm
from ..models import PublisherProfile, User, MonthYear, PublisherReport
import datetime


@authentication_required
def dashboard(response):
    publisher = response.user
    # if publisher.is_authenticated == False:
    #     return HttpResponseRedirect("/logout")

    # if publisher.publisherprofile.status == "Pending":
    #     return HttpResponseRedirect("/sign-up-suc")

    nav = "Dashboard"

    return render(response, "main/dashboard/dashboard.html", {"publisher": publisher, "nav": nav})


@authentication_required
@admin_privilege
def month_year(response):
    publisher = response.user
    # if publisher.is_authenticated == False:
    #     return HttpResponseRedirect("/logout")

    # if publisher.publisherprofile.status == "Pending":
    #     return HttpResponseRedirect("/sign-up-suc")

    # if not publisher.publisherprofile.privilege == "1":
    #     return HttpResponseRedirect("/logout")

    add_form = AddMonthYearForm(response.POST)
    if response.POST.get("add-month-year"):
        if add_form.is_valid():
            month = add_form.cleaned_data["month"]
            year = add_form.cleaned_data["year"]
            check_exist = MonthYear.objects.filter(
                month=month, year=year).count()
            if check_exist == 0 and year.isdigit() and len(month) > 0 and len(year) > 0:
                if add_form.cleaned_data["current"]:
                    MonthYear.objects.filter(
                        current=True).update(current=False)
                    l_current = True
                else:
                    l_current = False

                if add_form.cleaned_data["open"]:
                    open = True
                else:
                    open = False

                t = MonthYear(month=month, year=year,
                            current=l_current, open=open)
                t.save()
                return HttpResponseRedirect("/dashboard/month-year")
            else:
                return HttpResponseRedirect("/dashboard/month-year")
        else:
            AddMonthYearForm()

    if response.POST.get("edit-month-year"):
        id = response.POST.get('edit-id')
        Month_Year_model = MonthYear.objects.get(id=id)
        month = response.POST.get("month")
        year = response.POST.get("year")

        check_exist = MonthYear.objects.filter(
            month=month, year=year).exclude(id=id).count()
        if check_exist == 0 and year.isdigit() and len(month) > 0 and len(year) > 0:
            if response.POST.get("current"):
                MonthYear.objects.filter(current=True).update(current=False)
                l_current = True
            else:
                l_current = False

            if response.POST.get("open"):
                open = True
            else:
                open = False

            Month_Year_model.month = month
            Month_Year_model.year = year
            Month_Year_model.current = l_current
            Month_Year_model.open = open
            Month_Year_model.save()
            return HttpResponseRedirect("/dashboard/month-year")
        else:
            return HttpResponseRedirect("/dashboard/month-year")

    if response.POST.get('tag') == "delete":
        id = response.POST.get('id')

        MonthYear.objects.get(id=id).delete()

        if len(id) == 0:
            return HttpResponse(0)
        else:
            return HttpResponse(1)

    month_Year = MonthYear.objects.all().order_by('-id')

    return render(response, "main/dashboard/month-year.html", {"publisher": publisher, "add_form": add_form, "month_Year": month_Year})


def check_month_year(response):
    if response.POST.get('month_year_check'):
        month = response.POST.get('month')
        year = response.POST.get('year')
        if len(year) > 0:
            check_exist = MonthYear.objects.filter(
                month=month, year=year).count()
            if(year.isdigit()):
                if check_exist > 0:
                    return HttpResponse("taken")
                else:
                    return HttpResponse("not_taken")
            else:
                return HttpResponse("not_number")
        else:
            return HttpResponse(9)

    elif response.POST.get('month_year_check2'):
        month = response.POST.get('month')
        year = response.POST.get('year')
        id = response.POST.get('id')
        if len(year) > 0:
            check_exist = MonthYear.objects.filter(
                month=month, year=year).exclude(id=id).count()
            if(year.isdigit()):
                if check_exist > 0:
                    return HttpResponse("taken")
                else:
                    return HttpResponse("not_taken")
            else:
                return HttpResponse("not_number")
        else:
            return HttpResponse(9)

@authentication_required
@admin_privilege
def waiting_room(response):

    publisher = response.user
   

    if response.POST.get('tag') == "delete":
        id = response.POST.get('id')

        PublisherProfile.objects.get(user_id=id).delete()

        if len(id) == 0:
            return HttpResponse(0)
        else:
            return HttpResponse(1)

    pending_publishers = PublisherProfile.objects.filter(status="Pending")

    for pending_publisher in pending_publishers:
        # p = PublisherProfile.objects.filter(parent_id=pending_publisherw.username).exclude(username="JudeAFA5F6513")
        p = pending_publisher

    parent_names = PublisherProfile.objects.all()
    count_followers = PublisherProfile.objects.filter(status="Pending")

    return render(response, "main/dashboard/waiting-room.html", {"publisher": publisher, "pending_publishers": pending_publishers, "parent_names": parent_names, "count_followers": count_followers})

@authentication_required
def waiting_room_approve(response):
    publisher = response.user
    
    if response.method == 'POST':
        id = response.POST.get('unique_id')
        approve_model = PublisherProfile.objects.get(user_id=id)
        group = response.POST.get("group")

        if group == "Non-Publisher":
            pioneer = 0
            appointment = 0
        else:
            if response.POST.get("appoint"):
                appointment = response.POST.get("appoint")
            else:
                appointment = 0

            if response.POST.get("pioneer"):
                pioneer = 1
            else:
                pioneer = 0

        if len(group) > 0:
            approve_model.groupName = group
            approve_model.pioneer = pioneer
            approve_model.appointment = appointment
            approve_model.status = "Active"
            approve_model.updated_at = datetime.datetime.now()
            approve_model.save()
            return HttpResponseRedirect("/dashboard/waiting-room")
        else:
            return HttpResponseRedirect("/dashboard/waiting-room")

@authentication_required
def submit_report_select_month_year(response):
    publisher = response.user
    # if publisher.is_authenticated == False:
    #     return HttpResponseRedirect("/logout")

    # if publisher.publisherprofile.status == "Pending":
    #     return HttpResponseRedirect("/sign-up-suc")

    if response.session.get('id', None):
        del response.session['id']

    if response.method == 'POST':
        month = response.POST.get('Month')
        year = response.POST.get('Year')
        check = MonthYear.objects.filter(month=month, year=year).first()
        if check:
            response.session['id'] = check.id
            return HttpResponseRedirect("/submit-report")
        else:
            return HttpResponseRedirect("/submit-report/select-month-year")

    current = MonthYear.objects.filter(current=True)
    open = MonthYear.objects.filter(open=True)

    return render(response, "main/report/select-report-month-year.html", {"publisher": publisher, "current": current, "open": open})

@authentication_required
def submit_report(response):
    publisher = response.user
    # if publisher.is_authenticated == False:
    #     return HttpResponseRedirect("/logout")

    # if publisher.publisherprofile.status == "Pending":
    #     return HttpResponseRedirect("/sign-up-suc")

    if not response.session.get('id', None):
        return HttpResponseRedirect("/submit-report/select-month-year")

    month_year = MonthYear.objects.get(id=response.session['id'])

    my_publishers = PublisherProfile.objects.filter(
        parent_id=publisher.publisherprofile.username)
    my_publishers_add_form = PublisherProfile.objects.filter(
        parent_id=publisher.publisherprofile.username, status="Active").exclude(groupName="Non-Publisher")

    # reports = PublisherReport.objects.filter(month="January")

    return render(response, "main/report/submit-report.html", {"publisher": publisher, "month_year": month_year, "my_publishers": my_publishers, "my_publishers_add_form": my_publishers_add_form})

@authentication_required
def submit_report_post(response):

    publisher = response.user
    # if publisher.is_authenticated == False:
    #     return HttpResponseRedirect("/logout")

    # if publisher.publisherprofile.status == "Pending":
    #     return HttpResponseRedirect("/sign-up-suc")

    if not response.session.get('id', None):
        return HttpResponseRedirect("/submit-report/select-month-year")

    month_year = MonthYear.objects.get(id=response.session['id'])
    if response.POST.get('add_report'):
        publisher_username = response.POST.get('select_publisher')

        if response.POST.get('return_visit').isdigit():
            return_visit = int(response.POST.get('return_visit'))
        else:
            return_visit = 0

        if response.POST.get('bible_study').isdigit():
            bible_study = int(response.POST.get('bible_study'))
        else:
            bible_study = 0

        if response.POST.get('placements').isdigit():
            placements = int(response.POST.get('placements'))
        else:
            placements = 0

        if response.POST.get('video').isdigit():
            video = int(response.POST.get('video'))
        else:
            video = 0

        hours = int(response.POST.get('hours'))
        comments = response.POST.get('comments')

        publisher_info = PublisherProfile.objects.filter(
            username=publisher_username).first()
        check_duplicate_report = PublisherReport.objects.filter(
            publisher_username=publisher_username, month_year_id=month_year.id).count()
        if check_duplicate_report == 0:
            g = PublisherReport(publisher_username=publisher_info.username,
                                group=publisher_info.groupName,
                                pioneer=publisher_info.pioneer,
                                appointment=publisher_info.appointment,
                                month=month_year.month,
                                year=month_year.year,
                                month_year_id=month_year.id,
                                placements=placements,
                                video_showings=video,
                                hours=hours,
                                return_visits=return_visit,
                                bible_studies=bible_study,
                                comments=comments,
                                created_at=datetime.datetime.now())

            if int(bible_study) <= int(return_visit):
                g.save()

        # PublisherReport.objects.all().delete()
        return HttpResponseRedirect("/submit-report")

    if response.POST.get('tag') == "delete":
        id = response.POST.get('id')

        PublisherReport.objects.get(
            publisher_username=id, month_year_id=month_year.id).delete()

        if len(id) == 0:
            return HttpResponse(0)
        else:
            return HttpResponse(1)

@authentication_required
def submit_report_edit(response):

    publisher = response.user
    # if publisher.is_authenticated == False:
    #     return HttpResponseRedirect("/logout")

    # if publisher.publisherprofile.status == "Pending":
    #     return HttpResponseRedirect("/sign-up-suc")

    if not response.session.get('id', None):
        return HttpResponseRedirect("/submit-report/select-month-year")

    if response.POST.get('post_edit') == "1":

        id = response.POST.get('report_id')
        edit_report = PublisherReport.objects.get(id=id)

        if response.POST.get('return_visit').isdigit():
            return_visit = int(response.POST.get('return_visit'))
        else:
            return_visit = 0

        if response.POST.get('bible_study').isdigit():
            bible_study = int(response.POST.get('bible_study'))
        else:
            bible_study = 0

        if response.POST.get('placements').isdigit():
            placements = int(response.POST.get('placements'))
        else:
            placements = 0

        if response.POST.get('video').isdigit():
            video = int(response.POST.get('video'))
        else:
            video = 0

        hours = int(response.POST.get('hours'))
        comments = response.POST.get('comments')

        if int(bible_study) <= int(return_visit):
            edit_report.placements = placements
            edit_report.video_showings = video
            edit_report.hours = hours
            edit_report.return_visits = return_visit
            edit_report.bible_studies = bible_study
            edit_report.comments = comments
            edit_report.updated_at = datetime.datetime.now()
            edit_report.save()
        return HttpResponseRedirect("/submit-report")
    else:
        return HttpResponseRedirect("/submit-report")
