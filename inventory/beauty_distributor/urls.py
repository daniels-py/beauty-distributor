from django.urls import path
from django.http import HttpResponse
from .views import *

def simple_view(request):
    return HttpResponse('Funciona correctamente')

urlpatterns = [
    
        path('Principal/', Portada, name="Principal"),

]
