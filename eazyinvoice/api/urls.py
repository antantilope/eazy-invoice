
from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # HTML views
    path('', views.landing_page, name="page-landing"),
    path('login/', views.login_user, name="page-login"),
    path('logout/', views.logout_user, name="page-logout"),
    path('orgs/', views.orgs, name="page-orgs"),
    path('orgs/<slug:orgId>/', views.org, name="page-org"),
    path(
        'orgs/<slug:orgId>/invoice/<slug:invoiceId>/',
        views.download_invoice,
        name="page-invoice-download"
    ),

    # API views
    path(
        'api/orgs/<slug:orgId>/entry/new/',
        api_views.new_hours_entry,
        name="api-new-hours-entry",
    ),
    path(
        'api/orgs/<slug:orgId>/entry/<slug:entryId>/delete/',
        api_views.delete_hours_entry,
        name="api-delete-hours-entry",
    ),
    path(
        'api/orgs/<slug:orgId>/invoice/new/',
        api_views.create_invoice,
        name="api-create-invoice",
    ),
    path(
        'api/orgs/<slug:orgId>/invoice/<slug:invoiceId>/delete/',
        api_views.delete_invoice,
        name="api-delete-invoice",
    ),
    path(
        'api/orgs/<slug:orgId>/invoice/<slug:invoiceId>/paid/',
        api_views.mark_invoice_paid,
        name="api-delete-invoice",
    ),
]
