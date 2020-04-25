from django.shortcuts import render
from rest_framework import viewsets
from main.models import Report, File
from main.serializers import ReportSerializer, FileSerializer


class FileViewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class ReportViewset(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer