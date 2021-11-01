from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer


def index(request):
    return render(request, 'index.html', {})

