from django.shortcuts import render

from leads.models import Lead
from companies.models import Company
from contacts.models import Contact
from opportunities.models import Opportunity
from quotations.models import Quotation
from invoices.models import Invoice


def dashboard(request):
    context = {
        "lead_count": Lead.objects.count(),
        "company_count": Company.objects.count(),
        "contact_count": Contact.objects.count(),
        "opportunity_count": Opportunity.objects.count(),
        "quotation_count": Quotation.objects.count(),
        "invoice_count": Invoice.objects.count(),
    }

    return render(request, "dashboard_app/dashboard.html", context)