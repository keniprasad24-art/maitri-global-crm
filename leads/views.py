from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import openpyxl 
from .models import Lead

# 1. Lead List (Search सह)
def lead_list(request):
    query = request.GET.get("q", "")
    leads = Lead.objects.all().order_by('-id')
    if query:
        leads = leads.filter(Q(name_icontains=query) | Q(emailicontains=query) | Q(phone_icontains=query))
    
    paginator = Paginator(leads, 10)
    page_number = request.GET.get("page")
    leads = paginator.get_page(page_number)
    return render(request, "leads/lead_list.html", {"leads": leads, "query": query})

# 2. Add Lead
def add_lead(request):
    if request.method == "POST":
        Lead.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            company=request.POST.get("company"),
            source=request.POST.get("source"),
            status=request.POST.get("status"),
            lead_pdf=request.FILES.get("lead_pdf"),
        )
        return redirect("lead_list")

    return render(request, "leads/add_lead.html")
# 3. Edit Lead
def edit_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    if request.method == "POST":
        lead.name = request.POST.get("name")
        lead.email = request.POST.get("email")
        lead.phone = request.POST.get("phone")
        lead.company = request.POST.get("company")
        lead.source = request.POST.get("source")
        lead.status = request.POST.get("status")
        lead.save()
        return redirect("lead_list")
    return render(request, "leads/edit_lead.html", {"lead": lead})

# 4. Delete Lead
def delete_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    lead.delete()
    return redirect("lead_list")

# 5. Excel Upload 
def upload_leads_excel(request):
    if request.method == "POST":
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            messages.error(request, "Please select an Excel file.")
            return redirect('lead_list')
        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0]: 
                    Lead.objects.create(
                        name=str(row[0]),
                        email=str(row[1]) if row[1] else '',
                        phone=str(row[2]) if row[2] else '',
                        company=str(row[3]) if row[3] else 'Imported',
                        source='import',
                        status='New'
                    )
            messages.success(request, "Success! Leads uploaded successfully.")
            return redirect('lead_list')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('lead_list')
    return render(request, "leads/upload_excel.html")

# 6. Automation API (Facebook/WhatsApp साठी)
@csrf_exempt
def api_capture_lead(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            Lead.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                company=data.get('company', 'Online Inquiry'),
                source=data.get('source', 'website'),
                status='New'
            )
            return JsonResponse({"status": "success"}, status=201)
        except:
            return JsonResponse({"status": "error"}, status=400)
    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

# 7. Simulator
def lead_simulator(request):
    return render(request, "leads/lead_simulator.html")