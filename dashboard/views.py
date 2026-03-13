

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Dashboard Home Page Working")
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render
from .models import SensorData
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
from .models import SensorData

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

    for item in data:
        labels.append(item.timestamp.strftime("%H:%M:%S"))
        temps.append(item.value)

    return JsonResponse({
        "labels": labels,
        "temps": temps
    })




import openpyxl

def download_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sensor Data"

    # Header
    ws.append(["Timestamp", "Topic", "Value"])

    data = SensorData.objects.all()

    for d in data:
        ws.append([d.timestamp, d.topic, d.value])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="sensor_data.xlsx"'

    wb.save(response)
    return response

