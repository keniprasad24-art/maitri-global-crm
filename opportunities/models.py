from django.db import models
from companies.models import Company
from contacts.models import Contact

class Opportunity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=50)
    expected_close_date = models.DateField()

    def _str_(self):
        return self.title