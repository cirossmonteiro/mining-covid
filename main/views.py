from django.shortcuts import render
from rest_framework import viewsets
from main.models import Report
from main.serializers import ReportSerializer

# Create your views here.
class ReportViewset(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer