from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

import requests
from decouple import config

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def hello(request):
    return render(request, "hello/hello.html")

def counter(request):
    return render(request, "hello/counter.html")

def color(request):
    return render(request, "hello/color.html")

def color_selector(request):
    return render(request, "hello/color_selector.html")

def tasks(request):
    return render(request, "hello/tasks.html")

def currency(request):
    return render(request, "hello/currency.html")

@require_GET
def exchange_rates(request):
    API_KEY = config("EXCHANGE_RATES_API_KEY")
    url = f"http://api.exchangeratesapi.io/v1/latest"
    params = {
        "access_key": API_KEY,
        "symbols": "USD,AUD,CAD,PLN,MXN",
        "format": 1
    }
    try:
        response = requests.get(url, params=params)
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)