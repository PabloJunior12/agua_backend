from rest_framework import routers
from django.urls import path
# from .views import CompanyViewSet, YearViewSet, TotalDashboard, FinancialSummaryAPIView, PDFRecibosPorCalleApiView, DebtReportViewSet, CashViewSet, PaymentMethodViewSet, CustomerViewSet, ReadingViewSet, InvoiceViewSet, CategoryViewSet, ZonaViewSet, CalleViewSet, PDFGeneratorAPIView, PDFReciboApiView, CustomerUnpaidInvoicesView, ServiceViewSet, TariffViewSet
from .views import (
    CustomerViewSet, WaterMeterViewSet, CategoryViewSet, ViaViewSet, CalleViewSet, CashBoxViewSet,
    ReadingViewSet, InvoiceViewSet, ZonaViewSet, DebtViewSet, ReadingGenerationViewSet
)
router = routers.DefaultRouter()

# router.register("company", CompanyViewSet)
# router.register("year", YearViewSet)
# router.register("customer", CustomerViewSet)
# router.register("reading", ReadingViewSet)
# router.register("invoice", InvoiceViewSet)
router.register("categories", CategoryViewSet)
# router.register("zona", ZonaViewSet)
# router.register("calle", CalleViewSet)
# router.register("service", ServiceViewSet)
# router.register("tariff", TariffViewSet)
# router.register("cash", CashViewSet)
router.register("cash-box", CashBoxViewSet)
router.register('reading-generation', ReadingGenerationViewSet)
router.register('debts', DebtViewSet)
router.register('zonas', ZonaViewSet)
router.register('vias', ViaViewSet)
router.register('calles', CalleViewSet)
router.register('customers', CustomerViewSet)
router.register('meters', WaterMeterViewSet)
router.register('readings', ReadingViewSet)
router.register('invoices', InvoiceViewSet)

urlpatterns = [
#  path('customer/<str:dni>/unpaid-invoices/', CustomerUnpaidInvoicesView.as_view(), name='customer-unpaid-invoices'),
#  path('pdf/<int:invoice_id>', PDFGeneratorAPIView.as_view(), name='api_pdf'),
#  path('recibo/pdf/<int:reading_id>', PDFReciboApiView.as_view(), name='recibo_api_pdf'),
#  path('debt-reports/', DebtReportViewSet.as_view()),
#  path('receipts/by-address/<int:pk>/<str:periodo>', PDFRecibosPorCalleApiView.as_view()),
#  path("financial-summary/", FinancialSummaryAPIView.as_view(), name="financial-summary"),
#  path("invoices/summary/", TotalDashboard.as_view(), name="invoices-summary"),

] + router.urls