from django.shortcuts import render

# Create your views here.



def Portada(request):
    return render(request, "index.html")
