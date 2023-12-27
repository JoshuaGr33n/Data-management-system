from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

from .views import (
    views,
    views_dashboard,
    views_publishers,
    views_publisher_profile,
)
from .views.views_publisher_profile import SearchView



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

  path("dashboard/", views_dashboard.dashboard, name="dashboard"),
  path("dashboard/month-year", views_dashboard.month_year, name="month-year"),
  path("dashboard/check-month-year", views_dashboard.check_month_year, name="check-month-year"),
  path("dashboard/waiting-room", views_dashboard.waiting_room, name="waiting-room"),
  path("dashboard/waiting-room-approve", views_dashboard.waiting_room_approve, name="waiting-room-approve"),
  path("submit-report/select-month-year", views_dashboard.submit_report_select_month_year, name="submit-report-select-month-year"),
  path("submit-report/", views_dashboard.submit_report, name="submit-report"),
  path("submit-report-post/", views_dashboard.submit_report_post, name="submit-report-post"),
  path("submit-report-edit/", views_dashboard.submit_report_edit, name="submit-report-edit"),
  
  path("publishers/all-active-publishers", views_publishers.all_publishers, name="all-active-publishers"),
  path("publishers/non-publishers", views_publishers.non_publishers, name="non-publishers"),
  path("publishers/deactivated-publishers", views_publishers.deactivated_publishers, name="deactivated-publishers"),
  path("publishers/choose-category", views_publishers.choose_category, name="choose-category"),
  path("publishers/monthly-reports", views_publishers.monthly_report, name="monthly-reports"),
  # path("publishers/monthly-report-delete", views_publishers.monthly_report_delete, name="monthly-report-delete"),
  path("publishers/monthly-reports-stats", views_publishers.monthly_report_stats, name="monthly-reports-stats"),
  path("publishers/monthly-pending-reports", views_publishers.monthly_pending_report, name="monthly-pending-reports"),
  path("publishers/export-import-monthly-reports", views_publishers.export_import_monthly_report, name="export-import-monthly-reports"),
  path('export/csv/$', views_publishers.export_monthly_report_csv, name='export_monthly_report_csv'),
  path('export/xls/$', views_publishers.export_monthly_report_xls, name='export_monthly_report_xls'),
  path('publishers/import-excel', views_publishers.import_excel, name='import-excel'),
  path('publishers/delete-reports', views_publishers.delete_reports, name='delete-reports'),
  path('publishers/export-report-template', views_publishers.export_report__template_excel, name='export-report-template'),
  path('publishers/select-multiple-months-report', views_publishers.select_multiple_months, name='select-multiple-months-report'),
  path('publishers/multiple-months-report', views_publishers.multiple_months_report, name='multiple-months-report'),
  path('publishers/multiple-months-report-stats', views_publishers.multiple_months_report_stats, name='multiple-months-report-stats'),
  
  
  path("publisher-profile/<str:username>", views_publisher_profile.publisher_profile, name="publisher-profile"),
  path("publisher-profile/<str:username>/settings", views_publisher_profile.publisher_profile_settings, name="publisher-profile-settings"),
  path("publisher-profile/settings/update", views_publisher_profile.publisher_profile_settings_update, name="publisher-profile-settings-update-form"),
  path("publisher-profile/settings/update/password", views_publisher_profile.publisher_profile_settings_update_password, name="publisher-profile-settings-update-password-form"),
  path("publisher-profile/<str:username>/followers", views_publisher_profile.publisher_followers, name="publisher-profile-followers"),
  path("publisher-profile/follower/add", views_publisher_profile.add_follower, name="publisher-add-follower"),
  path('search/<str:username>/', SearchView.as_view(), name='search_view'),
  
   
]