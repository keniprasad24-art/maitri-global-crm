from django.db import models

class Lead(models.Model):
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('facebook', 'Facebook Ads'),
        ('whatsapp', 'WhatsApp'),
        ('manual', 'Manual Entry'),
    ]

    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Lost', 'Lost'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=100, default="Not Provided")
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='manual')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    lead_pdf = models.FileField(upload_to="lead_pdfs/", blank=True, null=True)

    def _str_(self):
        return self.name