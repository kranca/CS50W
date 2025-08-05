from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "react/react.html")

def counter(request):
    return render(request, "react/counter.html")

def addition(request):
    return render(request, "react/addition.html")