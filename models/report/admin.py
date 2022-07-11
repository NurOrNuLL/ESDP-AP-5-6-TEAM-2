from django.contrib import admin
from models.report.models import Report


class ReportAdmin(admin.ModelAdmin):
    class Meta:
        model = Report
