from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    source = models.CharField(max_length=50)

    def __str__(self):
        return self.name