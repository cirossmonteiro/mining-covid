from main.models import Report, File
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['path']


class ReportSerializer(serializers.ModelSerializer):
    # filetest = serializers.SlugRelatedField(read_only=True , slug_field='path')
    class Meta:
        model = Report
        fields = ['id', 'date', 'country', 'cases_total', 'cases_new',
            'deaths_total', 'deaths_new', 'transmission_type', 'days_last_case']
