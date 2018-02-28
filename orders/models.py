from django.db import models

# Create your models here.

class Medicines (models.Model):
    name = models.CharField(max_length=200)
    indication = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    drug_form = models.CharField(max_length=200)
    side_effects = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    manufacture = models.CharField(max_length=200)
    alternative_medicines = models.CharField(max_length=200)
