

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render

from dashboard.models import SensorData


def home(request):
    data = SensorData.objects.all().order_by('-timestamp')[:20]

    timestamps = [d.timestamp.strftime("%H:%M:%S") for d in data]
    temperatures = [d.temperature for d in data] 
    ph_values = [d.ph for d in data]
    turbidity_values = [d.turbidity for d in data]

    context = {
         "timestamps": timestamps, 
        "temperatures": temperatures, 
        "ph_values": ph_values, 
        "turbidity_values": turbidity_values  
        } 
    
    return render(request, 'home.html', context)

import json

def graph_view(request):
    data = SensorData.objects.all().order_by('-timestamp')[:50]
    data = reversed(data)

    timestamps = [d.timestamp.strftime("%H:%M:%S") for d in data]
    values = [float(d.temperature) for d in data]  # ensure float

    context = {
        'timestamps': json.dumps(timestamps),
        'values': json.dumps(values)
    }

    return render(request, 'graph.html', context)

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

def get_data(request):

    start = request.GET.get("start")
    end = request.GET.get("end")

    data = SensorData.objects.all()

    if start and end:
        start_time = parse_datetime(start)
        end_time = parse_datetime(end)
        data = data.filter(timestamp__range=(start_time, end_time))

    data = data.order_by("timestamp")

    labels = []
    temps = []
    ph_values = []
    turbidity_values = []

    for item in data:
        labels.append(item.timestamp.strftime("%H:%M:%S"))
        temps.append(item.temperature)
        ph_values.append(item.ph)
        turbidity_values.append(item.turbidity)


    return JsonResponse({
        "labels": labels,
        "temps": temps,
        "ph": ph_values,
        "turbidity": turbidity_values,
    })




import openpyxl

def download_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sensor Data"

    # Header
   

    data = SensorData.objects.all()
    ws.append(["Timestamp", "Temperature", "pH", "Turbidity"])

    data = SensorData.objects.all()

    for d in data:
        ws.append([d.timestamp, d.temperature, d.ph, d.turbidity])

    

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="sensor_data.xlsx"'

    wb.save(response)
    return response

