from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import api_root
from .auth_views import api_login, api_logout, api_user_info
from .pdf_views import InspectionReportPDFView, generate_inspection_report_pdf, get_report_pdf_data

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'equipment', views.EquipmentViewSet, basename='equipment')
router.register(r'users', views.UsersViewSet, basename='users')
router.register(r'checklist-items', views.ChecklistItemsViewSet, basename='checklist-items')
router.register(r'inspection-reports', views.InspectionReportsViewSet, basename='inspection-reports')
router.register(r'daily-inspection-data', views.DailyInspectionDataViewSet, basename='daily-inspection-data')
router.register(r'report-notes', views.ReportNotesViewSet, basename='report-notes')
router.register(r'report-attachments', views.ReportAttachmentsViewSet, basename='report-attachments')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    # Custom authentication endpoints
    path('api/auth/login/', api_login, name='api-login'),
    path('api/auth/logout/', api_logout, name='api-logout'),
    path('api/auth/user/', api_user_info, name='api-user-info'),
    # PDF generation endpoints
    path('api/reports/<int:report_id>/pdf/', generate_inspection_report_pdf, name='inspection-report-pdf'),
    path('api/reports/<int:report_id>/pdf-data/', get_report_pdf_data, name='inspection-report-pdf-data'),
    path('reports/<int:report_id>/pdf/', InspectionReportPDFView.as_view(), name='inspection-report-pdf-view'),
]