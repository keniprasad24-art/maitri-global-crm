from django.shortcuts import render, redirect
from .models import Opportunity
from .forms import OpportunityForm

def opportunity_list(request):
    opportunities = Opportunity.objects.all()
    return render(request, "opportunities/opportunity_list.html", {"opportunities": opportunities})

def add_opportunity(request):
    if request.method == "POST":
        form = OpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("opportunity_list")
    else:
        form = OpportunityForm()

    return render(request, "opportunities/add_opportunity.html", {"form": form})

def edit_opportunity(request, id):
    opportunity = Opportunity.objects.get(id=id)

    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect("opportunity_list")
    else:
        form = OpportunityForm(instance=opportunity)

    return render(request, "opportunities/add_opportunity.html", {"form": form})

def delete_opportunity(request, id):
    opportunity = Opportunity.objects.get(id=id)
    opportunity.delete()
    return redirect("opportunity_list")