from django.shortcuts import render, redirect
from .models import Medicines, Stores
from .forms import MedicineForm, StoreForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from dialogflow_lite.dialogflow import Dialogflow
from django.db import connection

import json

medicinesArr = [
{'name':'Thermol', 
'indication':'Fever,Headache','dosage':'Adult:  650mg in 3 times daily Maximum dose: 4 g / day',
'drug_form':'Paracetamol','side_effects':'Allergic reaction','price':'Rs.9.95','manufacture':'CDC','alternative_medicines':''},

{'name':'Febrinil', 'indication':'Fever,Headache','dosage':'650 mg in 2 times daily','drug_form':'Paracetamol',
'side_effects':'Allergic reaction',
'price':'Rs.16.98','manufacture':'Maneesh pharmaceuticals Ltd.','alternative_medicines':''},

{'name':'Medomol', 'indication':'Fever','dosage':'Adult: 500 - 1000 mg in 3 times daily Maximum dose: 4 g / day','drug_form':'Paracetamol','side_effects':
 'Allergic skin reaction,fatigue','price':'Rs.19.5','manufacture':'Medo Pharma','alternative_medicines':{'Thermol','Febrinil'}
},

 {'name':'Zoform', 'indication':'TypeII Diabetes Mellitus','dosage':'500mg Is to be taken after meals',
'drug_form':'Metformin','side_effects':'Vomiting','price':'Rs.11.68','manufacture':'FDC Ltd.','alternative_medicines':''},

{'name':'Glureg', 'indication':'TypeII Diabetes Mellitus','dosage':'500 mg:Is to be taken after meals',
'drug_form':'Metforminl','side_effects':'Nausea,Vomiting','price':'Rs.13.63','manufacture':'Medo pharma','alternative_medicines':''},
 
{'name':'Gluformin_G1', 'indication':'TypeII Diabetes Mellitus','dosage':
'Adults: Initial dose:250mg twice or thrice daily with meals.','drug_form':'metformin',
'side_effects':'Vomittin,Headache,Diarrhea','price':'Rs.22.30','manufacture':'Abbott Healthcare Pvt LTD',
'alternative_medicines':{'Zoform','Glureg'}}]

def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)

    return data

@login_required
@require_http_methods(['POST'])
def chat_view(request):
    dialogflow = Dialogflow(**settings.DIALOGFLOW)
    input_dict = convert(request.body)
    input_text = json.loads(input_dict)['text']
    responses = dialogflow.text_request(str(input_text))

    if request.method == "GET":
        # Return a method not allowed response
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status=405)
    elif request.method == "POST":
        
        data = {
            
            'text': responses[0],
        }
        print(str(input_text))
        out_str = ''
        MedicinesModel = Medicines.objects.all()
        for medicine in MedicinesModel:
            if str(input_text).find(medicine.name) != -1:
                print(medicine.name)
                out_str += 'Medicine Information --> ' + medicine.name +' :: '
                if medicine.alternative_medicines is not None:
                    out_str += 'Alternative Medicines --> ' + medicine.alternative_medicines +' :: '
                out_str += 'Medicine Indication --> '+medicine.indication
                AllStores = Stores.objects.all()
                out_str += ':: Medicine are available at store --> '
                for store in AllStores:
                    #print('store available'+store.medicines_available)
                    if str(medicine.name) in store.medicines_available:
                        out_str += 'Store Name: '+store.name + ' Address: '+store.address
                        print('store available')
                data = {
                'text': out_str,
                }
        
        return JsonResponse(data, status=200)
    elif request.method == "PATCH":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    elif request.method == "DELETE":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

@login_required
def index(request):
    MedicinesCount = Medicines.objects.all().count()
    print(MedicinesCount)
    if MedicinesCount == 0:
        insertAllRecords()

    MedicinesModel = Medicines.objects.all()
    return render(request, 'index.html', {'medicines': MedicinesModel})

@login_required
def storeList(request):
    StoresList = Stores.objects.all()
    return render(request, 'index_store.html', {'stores': StoresList})

def insertAllRecords():
    for medicine in medicinesArr:
        strigConcatVal = ','.join(medicine['alternative_medicines'])
        print(medicine['alternative_medicines'])
        Medicines.objects.create(name = medicine['name'],
        indication = medicine['indication'],
        dosage = medicine['dosage'],
        drug_form = medicine['drug_form'],
        side_effects = medicine['side_effects'],
        price = medicine['price'],
        manufacture = medicine['manufacture'],
        alternative_medicines = strigConcatVal)


@login_required
def show(request, medicine_name):
    MedicinesModel = Medicines.objects.filter(name=medicine_name)
    alternativeTemp=[i.alternative_medicines for i in  MedicinesModel]
   
    for altMedArr in alternativeTemp:
        medicineAlternative = altMedArr.split(",")
  
    fullMedicinesModel = Medicines.objects.all()
    
    return render(request, 'show.html', {'medicineAlternative': medicineAlternative, 'medicines': fullMedicinesModel})

@login_required
def new(request):
    if request.POST:
        #form = MedicineForm(request.POST)
        #print(request.POST.getlist('alternative_medicines'))
        requestData = request.POST.getlist('alternative_medicines')
        medicineName = request.POST.get('name')
        nameAltered = medicineName.replace(" ","_")
        form = request.POST.copy()
        #print(','.join(requestData))
        if requestData:
            print("Dict is not Empty")
            strigConcatVal = ','.join(requestData)
            form["alternative_medicines"] = strigConcatVal

        form["name"] = nameAltered
        form = MedicineForm(form)
        if form.is_valid():
            if form.save():
                return redirect('/order/new/', messages.success(request, 'Medicine successfully created.', 'alert-success'))
            else:
                return redirect('/order/new/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/order/new/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = MedicineForm()
        MedicinesModel = Medicines.objects.all()
        return render(request, 'new.html', {'form':form, 'medicines': MedicinesModel})


@login_required
def newStore(request):
    if request.POST:
        #form = MedicineForm(request.POST)
        #print(request.POST.getlist('alternative_medicines'))
        requestData = request.POST.getlist('medicines_available')
        #print(','.join(requestData))
        strigConcatVal = ','.join(requestData)
        print(strigConcatVal)
        form = request.POST.copy()
        form["medicines_available"] = strigConcatVal
        form = StoreForm(form)
        if form.is_valid():
            if form.save():
                return redirect('/order/newStore/', messages.success(request, 'Store successfully created.', 'alert-success'))
            else:
                return redirect('/order/newStore/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/order/newStore/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = StoreForm()
        MedicinesModel = Medicines.objects.all()
        return render(request, 'new_store.html', {'form':form, 'medicines': MedicinesModel})

def poi_list(request):
    store = Stores.objects.all()
    return render(request, 'position_list.html', {'Stores': store})