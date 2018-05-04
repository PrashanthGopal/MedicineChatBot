from django.db import models
from geoposition.fields import GeopositionField

# Create your models here.

class Medicines (models.Model):
    name = models.CharField(max_length=200)
    indication = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    drug_form = models.CharField(max_length=200)
    side_effects = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    manufacture = models.CharField(max_length=200)
    alternative_medicines = models.CharField(max_length=500, blank=True, null=True)


class Stores (models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    Landmark = models.CharField(max_length=50)
    medicines_available = models.CharField(max_length=500)
    position = GeopositionField(blank=True)
    #position = GeopositionField(widget=GeopositionWidget(mapOptions={'scrollwheel': False,}), required=False)
