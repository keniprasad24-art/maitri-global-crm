from django.shortcuts import render

from leads.models import Lead
from companies.models import Company
from opportunities.models import Opportunity
from quotations.models import Quotation
from invoices.models import Invoice
from qualified.models import Qualified
from subscription.models import Subscription
from django.db.models import Count
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    recent_leads = Lead.objects.order_by('-id')[:5]
lead_chart_labels = ["New", "Qualified", "Lost"]
lead_chart_data = [
    Lead.objects.filter(status="New").count(),
    Lead.objects.filter(status="Qualified").count(),
    Lead.objects.filter(status="Lost").count(),
]

opp_chart_labels = ["Open", "Won", "Lost"]
from django.shortcuts import render

from leads.models import Lead
from companies.models import Company
from opportunities.models import Opportunity
from quotations.models import Quotation
from invoices.models import Invoice
from qualified.models import Qualified
from subscription.models import Subscription
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    recent_leads = Lead.objects.order_by('-id')[:5]

    lead_chart_labels = ["New", "Qualified", "Lost"]
    lead_chart_data = [
        Lead.objects.filter(status="New").count(),
        Lead.objects.filter(status="Qualified").count(),
        Lead.objects.filter(status="Lost").count(),
    ]

    opp_chart_labels = ["Open", "Won", "Lost"]
    opp_chart_data = [
        Opportunity.objects.filter(status="Open").count(),
        Opportunity.objects.filter(status="Won").count(),
        Opportunity.objects.filter(status="Lost").count(),
    ]

    context = {
        "lead_count": Lead.objects.count(),
        "company_count": Company.objects.count(),
        "opportunity_count": Opportunity.objects.count(),
        "quotation_count": Quotation.objects.count(),
        "invoice_count": Invoice.objects.count(),
        "qualified_count": Qualified.objects.count(),

        "won_count": Opportunity.objects.filter(status="Won").count(),
        "lost_count": Opportunity.objects.filter(status="Lost").count(),

        "total_subscriptions": Subscription.objects.count(),
        "active_subscriptions": Subscription.objects.filter(status="Active").count(),
        "expired_subscriptions": Subscription.objects.filter(status="Expired").count(),

        "lead_chart_labels": lead_chart_labels,
        "lead_chart_data": lead_chart_data,
        "opp_chart_labels": opp_chart_labels,
        "opp_chart_data": opp_chart_data,

        "recent_leads": recent_leads,
    }

    return render(request, "dashboard_app/dashboard.html", context)