from django import template
from random import randint
from ..models import PublisherProfile, PublisherReport
from django.utils import timezone
import math

register = template.Library()


@register.simple_tag
def random_number():
    return randint(0, 999)


@register.simple_tag
def gold():
    return "Gold"


@register.simple_tag
def setPioneer(val=None):
    return val


@register.simple_tag
def setAppointment(val=None):
    return val


@register.simple_tag
def get_fields_task_name(kind):
    return kind


@register.simple_tag()
def count_followers(username):
    count = PublisherProfile.objects.filter(
        parent_id=username).exclude(username=username).count()
    return count


@register.simple_tag()
def submit_report_get_publisher_report(username, month_year_id):
    report = PublisherReport.objects.filter(
        publisher_username=username, month_year_id=month_year_id)
    return report


@register.simple_tag()
def check_my_publishers(username, month_year_id):
    report = PublisherReport.objects.filter(
        publisher_username=username, month_year_id=month_year_id).count()
    return report


@register.simple_tag()
def check_month_year_content(month_year_id):
    result = PublisherReport.objects.filter(
        month_year_id=month_year_id).count()
    return result


@register.simple_tag
def waiting_room_notifications():
    result = PublisherProfile.objects.filter(status="Pending").count()
    return result


@register.simple_tag
def waiting_room_notifications_top_5():
    result = PublisherProfile.objects.filter(status="Pending")[:5]
    return result


@register.simple_tag
def time_ago(created_at):
    now = timezone.now()

    diff = now - created_at

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        seconds = diff.seconds

        if seconds == 1:
            return str(seconds) + " second ago"

        else:
            return str(seconds) + " seconds ago"

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        minutes = math.floor(diff.seconds/60)

        if minutes == 1:
            return str(minutes) + " minute ago"

        else:
            return str(minutes) + " minutes ago"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        hours = math.floor(diff.seconds/3600)

        if hours == 1:
            return str(hours) + " hour ago"

        else:
            return str(hours) + " hours ago"

    # 1 day to 30 days
    if diff.days >= 1 and diff.days < 30:
        days = diff.days

        if days == 1:
            return str(days) + " day ago"

        else:
            return str(days) + " days ago"

    if diff.days >= 30 and diff.days < 365:
        months = math.floor(diff.days/30)

        if months == 1:
            return str(months) + " month ago"

        else:
            return str(months) + " months ago"

    if diff.days >= 365:
        years = math.floor(diff.days/365)

        if years == 1:
            return str(years) + " year ago"

        else:
            return str(years) + " years ago"


@register.simple_tag
def publisher_report_name(username):
    result = PublisherProfile.objects.get(username=username)
    return result


@register.simple_tag
def publisher_status_tag(username):
    publisher = PublisherProfile.objects.get(username=username)
    if publisher.groupName == "Non-Publisher":
        return 'fas fa-user text-secondary mr-2'
    else:
        if publisher.status == "Active":
            return 'fas fa-check-circle text-success mr-2'
        elif publisher.status == "Pending":
            return 'fas fa-check-circle text-warning mr-2'
        elif publisher.status == "Deactivated":
            return 'fas fa-times-circle text-danger mr-2'
        else:
            return ''


@register.simple_tag
def pending_report_query(username, month_year_id):
    report = PublisherReport.objects.filter(
        publisher_username=username, month_year_id=month_year_id).count()
    return report

 
    
