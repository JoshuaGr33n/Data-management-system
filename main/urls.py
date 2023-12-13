from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('sign-up/', views.signup_view, name="sign-up"),
    path('sign-up-suc/', views.sign_up_suc, name="sign-up-suc"),
    path('update-acct-pending-details/', views.update_acct_pending_details, name="update-acct-pending-details"),
    path('check-follower-phone-exist/', views.check_follower_phone_exist, name="check-follower-phone-exist"),
    path('delete-follower/', views.delete_follower, name="delete-follower"),
     path('sign-up-suc/acct-pen-details/', views.acct_pen_details, name="acct-pen-details"),
    path('login/', LoginView.as_view(
    authentication_form=CustomLoginForm),
    name="login"
  ),
   path('sign-up-suc-redirect/', views.sign_up_suc_redirect, name="sign-up-suc-redirect"),

  path("dashboard/", views.dashboard, name="dashboard"),
  path("dashboard/month-year", views.month_year, name="month-year"),
  path("dashboard/check-month-year", views.check_month_year, name="check-month-year"),
  path("dashboard/waiting-room", views.waiting_room, name="waiting-room"),
  path("dashboard/waiting-room-approve", views.waiting_room_approve, name="waiting-room-approve"),
  path("submit-report/select-month-year", views.submit_report_select_month_year, name="submit-report-select-month-year"),
  path("submit-report/", views.submit_report, name="submit-report"),
  path("submit-report-post/", views.submit_report_post, name="submit-report-post"),
  path("submit-report-edit/", views.submit_report_edit, name="submit-report-edit"),
  path("publishers/all-active-publishers", views.all_publishers, name="all-active-publishers"),
  path("publishers/non-publishers", views.non_publishers, name="non-publishers"),
  path("publishers/deactivated-publishers", views.deactivated_publishers, name="deactivated-publishers"),
  path("publisher-profile/<str:username>", views.publisher_profile, name="publisher-profile"),
  path("publishers/choose-category", views.choose_category, name="choose-category"),
  path("publishers/monthly-reports", views.monthly_report, name="monthly-reports"),
  # path("publishers/monthly-report-delete", views.monthly_report_delete, name="monthly-report-delete"),
  path("publishers/monthly-reports-stats", views.monthly_report_stats, name="monthly-reports-stats"),
  path("publishers/monthly-pending-reports", views.monthly_pending_report, name="monthly-pending-reports"),
  path("publishers/export-import-monthly-reports", views.export_import_monthly_report, name="export-import-monthly-reports"),
  path('export/csv/$', views.export_monthly_report_csv, name='export_monthly_report_csv'),
  path('export/xls/$', views.export_monthly_report_xls, name='export_monthly_report_xls'),
  path('publishers/import-excel', views.import_excel, name='import-excel'),
   path('publishers/delete-reports', views.delete_reports, name='delete-reports'),
   
]