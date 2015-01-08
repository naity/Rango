from django.shortcuts import render

# Create your views here.
def index(request):
    context = {"boldmessage": "I am bold font from the context"}
    return render(request, "rango/index.html", context)

def about(request):
    return render(request, "rango/about.html")