from django.shortcuts import render, redirect
from .models import Medicines
from .forms import MedicineForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from dialogflow_lite.dialogflow import Dialogflow

import json

medicines = [{'name':'Medomol', 'indication':'Fever','dosage':'Adult: 500 - 1000 mg in 3 times daily Maximum dose: 4 g / day','drug_form':'Paracetamol','side_effects':
 'Allergic skin reaction,fatigue','price':'Rs.19.5','manufacture':'Medo Pharma','alternative_medicines':[{'name':'Thermol', 'indication':'Fever,Headache','dosage':'Adult:  650mg in 3 times daily Maximum dose: 4 g / day','drug_form':'Paracetamol','side_effects':'Allergic reaction','price':'Rs.9.95','manufacture':'CDC'},
{'name':'Febrinil', 'indication':'Fever,Headache','dosage':'650 mg in 2 times daily','drug_form':'Paracetamol','side_effects':'Allergic reaction','price':'Rs.16.98','manufacture':'Maneesh pharmaceuticals Ltd.'}]},

{'name':'Gluformin_G1', 'indication':'TypeII Diabetes Mellitus','dosage':'Adults: Initial dose:250mg twice or thrice daily with meals.','drug_form':'metformin','side_effects':'Vomittin,Headache,Diarrhea','price':'Rs.22.30','manufacture':'Abbott Healthcare Pvt LTD','alternative_medicines':[{'name':'Zoform,', 'indication':'TypeII Diabetes Mellitus','dosage':'500mg Is to be taken after meals',
'drug_form':'Metformin','side_effects':'Vomiting','price':'Rs.11.68','manufacture':'FDC Ltd.'},
{'name':'Glureg', 'indication':'TypeII Diabetes Mellitus','dosage':'500 mg:Is to be taken after meals',
'drug_form':'Metforminl','side_effects':'Nausea,Vomiting','price':'Rs.13.63','manufacture':'Medo pharma'}]},

{'name':'Pan_40', 'indication':'Acidity,Heart burn','dosage':'10-15 minutes before taking food.',
'drug_form':'Pantoprazole','side_effects':'Altered sense of taste,skin rash','price':'Rs.138','manufacture':'Aeran India Pvt. Ltd.',
 'alternative_medicines':[{'name':'Topp', 'indication':'Acidity,Heart burn','dosage':'40mg: with or without food',
 'drug_form':'Pantoprazole','side_effects':'Headache,Nausea','price':'Rs.20','manufacture':'Systopic Laboratories  Pvt Ltd.'},
{'name':'Zipant', 'indication':'Acidity,Heart burn','dosage':'40mg:20 minutes before taking food','drug_form':'Pantoprazole',
'side_effects':'Fatigue,diarrhoeae','price':'Rs.36.15','manufacture':'FDC Pvt Ltd.'}]},

{'name':'Teleact', 'indication':'High Blood Pressure','dosage':'40mg once dailyMaintenance dose: 20to 80mg once daily ',
'drug_form':'Telmisartan','side_effects':'Back pain,Muscle pain','price':'Rs.66.97','manufacture':'Ranbaxy Laboratories Ltd.',
 'alternative_medicines':[{'name':'Ozotel', 'indication':'High Blood Pressure,Hypertension','dosage':'40mg:with or without food',
 'drug_form':'Telmisartan','side_effects':'Dizziness,back pain','price':'Rs.30','manufacture':'Ozone pharmaceuticals Ltd.'},
{'name':'Zimtel', 'indication':'Abdominal pain,Fever','dosage':'20mg:with or without food','drug_form':'Telmisartan',
'side_effects':'Sinus inflammation,back pain','price':'Rs.12','manufacture':'Zim Laboratories Ltd.'}]},

{'name':'Nico_Droxil', 'indication':'Bacterial Infection','dosage':'the recommended daily dosage for children is 30 mg/kg/day in a single dose or in equally divided doses every 12 hours.',
'drug_form':'Cefadroxil1','side_effects':'Stomach pain,indigestion','price':'Rs.15','manufacture':'Abbott Healthcare Pvt. Ltd.',
 'alternative_medicines':[{'name':'Droxyl', 'indication':'Bacterial Infection','dosage':'500mg:with or without food',
 'drug_form':'Cefadroxil','side_effects':'Nausea,allergic reaction','price':'Rs.40.99','manufacture':'Torrent pharmaceuticals Ltd.'},
 {'name':'Odoxil', 'indication':'Bacterial Infection','dosage':'500mg:with  food',
 'drug_form':'Cefadroxil','side_effects':'Nausea,allergic reaction','price':'Rs.40.67','manufacture':'Lupin Ltd.'}]},
 
 {'name':'Zapiz', 'indication':'Treat panic attacks and sleep disorders','dosage':'Adult: Anticonvulsant:Initial dose: 0.5 mg three times a day',
 'drug_form':'Clonazepam','side_effects':'Depresssion,allergy','price':'Rs.31.58','manufacture':'Intas Pharmaceuticals Ltd.',
 'alternative_medicines':[{'name':'Cozil', 'indication':'Treat panic attacks and sleep disorders','dosage':'5mg:with or without food',
 'drug_form':'Clonazepam','side_effects':'Sleepiness,fatigue,headache','price':'Rs.12','manufacture':'Medico Lab '},
{'name':'Clone', 'indication':'Treat panic attacks and sleep disorders','dosage':'2mg:with or without food','drug_form':'Clonazepam',
'side_effects':'Sleepiness,fatigue,headache','price':'Rs.36.07','manufacture':'VGR  bio Lab '}]},

{'name':'Cyclopam', 'indication':'Abdominal pain,','dosage':'Adult: Oral: 80 mg / day in 4 divided doses 30 - 60 minutes before meals',
'drug_form':'Dicyclomine','side_effects':'Nausea,weakness,blurred vision','price':'Rs.43','manufacture':'Indoco Remedies Ltd.',
 'alternative_medicines':[{'name':'Colimex', 'indication':'Abdominal pain','dosage':'20/500mg:Compulsolury after meals',
 'drug_form':'Dicyclomile','side_effects':'Blurred vision,weakness','price':'Rs.25','manufacture':'Wallace pharmaceuticals Ltd.'},
{'name':'Cyclo_P', 'indication':'Abdominal pain','dosage':'20mg:after  meals','drug_form':'Cyclo P 20/500mg',
'side_effects':'Nausea,nervousness','price':'Rs.Rs.3.75','manufacture':'Laborate pharmaceuticals India Ltd'}]},

{'name':'Amaryl', 'indication':'TypeII diabetes','dosage':'Initial: 1-2 mg  after breakfast or with first meal; may increase dose by 1-2 mg every 1-2 weeks; not to exceed 8 mg/day',
'drug_form':'Glimepiride','side_effects':'Anemia,Jaundice','price':'Rs.109','manufacture':'Sanofi India Ltd.',
 'alternative_medicines':[{'name':'K-Glim', 'indication':'TypeII diabetes','dosage':'2mg:with food',
 'drug_form':'Glimepiride','side_effects':'Low blood Sugar Levels,dizziness','price':'Rs.28.35','manufacture':'Blue Cross Laborotaries Ltd.'},
{'name':'Febrinil', 'indication':'TypeII diabetes','dosage':'1mg:with food','drug_form':'Glimepiride',
'side_effects':'Low blood Sugar Levels,dizziness','price':'Rs.14.44','manufacture':'FDC Ltd.'}]}
]

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
    
    return render(request, 'index.html', {'medicines': medicines})

@login_required
def show(request, medicine_name):
    medicineAlternative = dict()
    alternativeTemp = dict()
    for medicine in medicines:
        if medicine['name'] == medicine_name:
            medicineAlternative = medicine['alternative_medicines']


    return render(request, 'show.html', {'medicineAlternative': medicineAlternative})

@login_required
def new(request):
    if request.POST:
        form = MedicineForm(request.POST)
        if form.is_valid():
            if form.save():
                return redirect('/', messages.success(request, 'Order was successfully created.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = MedicineForm()
        return render(request, 'new.html', {'form':form})

