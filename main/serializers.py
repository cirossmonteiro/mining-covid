from main.models import Report
from rest_framework import serializers

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'date', 'country', 'cases_total', 'cases_new',
            'deaths_total', 'deaths_new', 'transmission_type', 'days_last_case']
