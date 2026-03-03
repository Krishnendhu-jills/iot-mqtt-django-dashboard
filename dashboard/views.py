

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

   