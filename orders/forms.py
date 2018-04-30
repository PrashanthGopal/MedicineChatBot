from django.forms import ModelForm
from django import forms
from .models import Medicines, Stores

class MedicineForm(ModelForm):
    
        
    class Meta:
        model = Medicines
        fields = ['name','indication','dosage','drug_form','side_effects','price','manufacture','alternative_medicines']

class StoreForm(ModelForm):
            
    class Meta:
        model = Stores
        fields = ['name','owner_name','position','address','Landmark','medicines_available']
