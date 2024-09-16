from django.urls import path

from core.reports.views import ReportSaleView

urlpatterns = [
    # reports
    path('reports/sale/', ReportSaleView.as_view(), name='sale_report'),
]