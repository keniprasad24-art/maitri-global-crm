from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import openpyxl
from .models import Lead


def lead_list(request):
    query = request.GET.get("q", "")
    leads = Lead.objects.all().order_by("-id")

    if query:
        leads = leads.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(client_name__icontains=query)
            | Q(email_id__icontains=query)
            | Q(mobile_no__icontains=query)
        )

    paginator = Paginator(leads, 10)
    page_number = request.GET.get("page")
    leads = paginator.get_page(page_number)

    return render(
        request,
        "leads/lead_list.html",
        {"leads": leads, "query": query},
    )


def add_lead(request):
    if request.method == "POST":
        Lead.objects.create(
            name=request.POST.get("name", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
            company=request.POST.get("company", ""),
            source=request.POST.get("source", "manual"),
            status=request.POST.get("status", "New"),
            lead_pdf=request.FILES.get("lead_pdf"),
        )
        return redirect("lead_list")

    return render(request, "leads/add_lead.html")


def edit_lead(request, id):
    lead = get_object_or_404(Lead, id=id)

    if request.method == "POST":
        lead.name = request.POST.get("name", "")
        lead.email = request.POST.get("email", "")
        lead.phone = request.POST.get("phone", "")
        lead.company = request.POST.get("company", "")
        lead.source = request.POST.get("source", "manual")
        lead.status = request.POST.get("status", "New")
        lead.save()
        return redirect("lead_list")

    return render(request, "leads/edit_lead.html", {"lead": lead})


def delete_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    lead.delete()
    return redirect("lead_list")


# Excel import: 21-column CRM Excel
def upload_leads_excel(request):
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")

        if not excel_file:
            messages.error(request, "Please select an Excel file.")
            return redirect("lead_list")

        try:
            wb = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = wb.active

            imported_count = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row or all(value in (None, "") for value in row):
                    continue

                values = list(row) + [None] * max(0, 21 - len(row))

                sr_no = values[0]
                current_requirements = values[1]
                lead_received_date = values[2]
                lead_source = values[3]
                reference_name = values[4]
                client_name = values[5]
                end_client = values[6]
                location = values[7]
                contact_person = values[8]
                designation = values[9]
                mobile_no = values[10]
                email_id = values[11]
                one_time_recurring = values[12]
                project_duration = values[13]
                consultant_name = values[14]
                consultant_cost = values[15]
                maitri_margin = values[16]
                lead_stage = values[17]
                next_follow_up_date = values[18]
                vendor_working_on = values[19]
                status = values[20]

                # Required display fields
                name_value = str(client_name or "").strip()
                email_value = str(email_id or "").strip()
                phone_value = str(mobile_no or "").strip()
                company_value = str(end_client or client_name or "Not Provided").strip()

                # Do not create completely empty lead rows.
                if not name_value and not email_value and not phone_value:
                    continue

                Lead.objects.create(
                    sr_no=int(sr_no) if isinstance(sr_no, (int, float)) else 0,
                    current_requirements=str(current_requirements or ""),
                    lead_received_date=lead_received_date,
                    lead_source=str(lead_source or ""),
                    reference_name=str(reference_name or ""),
                    client_name=name_value,
                    end_client=str(end_client or ""),
                    location=str(location or ""),
                    contact_person=str(contact_person or ""),
                    designation=str(designation or ""),
                    mobile_no=phone_value,
                    email_id=email_value,
                    one_time_recurring=str(one_time_recurring or ""),
                    project_duration=str(project_duration or ""),
                    consultant_name=str(consultant_name or ""),
                    consultant_cost=consultant_cost if consultant_cost not in (None, "") else None,
                    maitri_margin=maitri_margin if maitri_margin not in (None, "") else None,
                    lead_stage=str(lead_stage or ""),
                    next_follow_up_date=next_follow_up_date,
                    vendor_working_on=str(vendor_working_on or ""),
                    status=str(status or "New"),

                    # These are the fields used by the existing Lead List.
                    name=name_value,
                    email=email_value,
                    phone=phone_value,
                    company=company_value,
                    source="import",
                )

                imported_count += 1

            messages.success(
                request,
                f"{imported_count} leads uploaded and saved successfully.",
            )
            return redirect("lead_list")

        except Exception as e:
            messages.error(request, f"Excel upload failed: {e}")
            return redirect("lead_list")

    return render(request, "leads/upload_excel.html")


@csrf_exempt
def api_capture_lead(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            Lead.objects.create(
                name=data.get("name", ""),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                company=data.get("company", "Online Inquiry"),
                source=data.get("source", "website"),
                status="New",
            )

            return JsonResponse({"status": "success"}, status=201)

        except Exception:
            return JsonResponse({"status": "error"}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Only POST allowed"},
        status=405,
    )


def lead_simulator(request):
    return render(request, "leads/lead_simulator.html")
