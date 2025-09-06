from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import api_root

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
]