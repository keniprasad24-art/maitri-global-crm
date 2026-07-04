"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("dashboard_app.urls")),
    path("admin/", admin.site.urls),

    # Companies
    path("companies/", include("companies.urls")),

    # Contacts
    path("contacts/", include("contacts.urls")),

    # Leads
    path("leads/", include("leads.urls")),

    # Opportunities
    path("opportunities/", include("opportunities.urls")),

    # Quotations
    path("quotations/", include("quotations.urls")),
    path("invoices/", include("invoices.urls")),
]