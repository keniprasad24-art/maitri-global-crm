from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from companies.models import Company


def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/contact_list.html", {"contacts": contacts})


def add_contact(request):
    companies = Company.objects.all()

    if request.method == "POST":
        Contact.objects.create(
            company=Company.objects.get(id=request.POST["company"]),
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
        )
        return redirect("contact_list")

    return render(request, "contacts/add_contact.html", {
    "companies": companies
})
def edit_contact(request, id):
   contact = get_object_or_404(Contact, id=id)
   return render(request, "contacts/add_contact.html", {
        "contact": contact,
        "companies": Company.objects.all()
    })

def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect("contact_list") 