import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "scroll/index.html")

def scroll(request):
    return render(request, "scroll/scroll.html", {
        "numbers" : range(1, 101)
    })

def posts(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    time.sleep(0.5)

    return JsonResponse({
        "posts" : data
    })

def hide(request):
    return render(request, "scroll/hide.html")