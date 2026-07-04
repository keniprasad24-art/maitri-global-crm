from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Lead


def lead_list(request):
    leads = Lead.objects.all()
    return render(request, "leads/lead_list.html", {"leads": leads})


def add_lead(request):
    return HttpResponse("Add Lead Page")


def edit_lead(request, id):
    lead = get_object_or_404(Lead, id=id)

    if request.method == "POST":
        lead.name = request.POST["name"]
        lead.email = request.POST["email"]
        lead.phone = request.POST["phone"]
        lead.company = request.POST["company"]
        lead.source = request.POST["source"]
        lead.status = request.POST["status"]
        lead.save()
        return redirect("lead_list")

    return render(request, "leads/edit_lead.html", {"lead": lead})


def add_lead(request):
    if request.method == "POST":
        Lead.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            company=request.POST["company"],
            source=request.POST["source"],
            status=request.POST["status"],
        )
        return redirect("lead_list")

    return render(request, "leads/add_lead.html")
def delete_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    lead.delete()
    return redirect("lead_list")