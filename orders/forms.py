from django.forms import ModelForm
from django import forms
from .models import Medicines

class MedicineForm(ModelForm):
    
        
    class Meta:
        model = Medicines
        fields = ['name','indication','dosage','drug_form','side_effects','price','manufacture','alternative_medicines']

