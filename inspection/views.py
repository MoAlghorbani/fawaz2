from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime, date, timedelta

from .models import (
    Equipment, Users, ChecklistItems, InspectionReports,
    DailyInspectionData, ReportNotes, ReportAttachments
)
from .serializers import (
    EquipmentSerializer, UsersSerializer, ChecklistItemsSerializer,
    InspectionReportsSerializer, InspectionReportsListSerializer,
    DailyInspectionDataSerializer, ReportNotesSerializer, ReportAttachmentsSerializer
)


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Equipment model with full CRUD operations.
    
    Available endpoints:
    - GET /api/equipment/ - List all equipment
    - POST /api/equipment/ - Create new equipment
    - GET /api/equipment/{id}/ - Retrieve specific equipment
    - PUT /api/equipment/{id}/ - Update equipment
    - PATCH /api/equipment/{id}/ - Partial update equipment
    - DELETE /api/equipment/{id}/ - Delete equipment
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'equipment_type']
    search_fields = ['serial_number', 'equipment_type', 'model']
    ordering_fields = ['equipment_id', 'serial_number', 'equipment_type', 'model']
    ordering = ['equipment_type', 'serial_number']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active equipment."""
        active_equipment = self.queryset.filter(status='active')
        serializer = self.get_serializer(active_equipment, many=True)
        return Response(serializer.data)


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Users model with full CRUD operations.
    
    Available endpoints:
    - GET /api/users/ - List all users
    - POST /api/users/ - Create new user
    - GET /api/users/{id}/ - Retrieve specific user
    - PUT /api/users/{id}/ - Update user
    - PATCH /api/users/{id}/ - Partial update user
    - DELETE /api/users/{id}/ - Delete user
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role']
    search_fields = ['full_name', 'employee_number']
    ordering_fields = ['user_id', 'full_name', 'role', 'employee_number']
    ordering = ['full_name']

    @action(detail=False, methods=['get'])
    def operators(self, request):
        """Get only operators."""
        operators = self.queryset.filter(role='operator')
        serializer = self.get_serializer(operators, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def supervisors(self, request):
        """Get only supervisors."""
        supervisors = self.queryset.filter(role='supervisor')
        serializer = self.get_serializer(supervisors, many=True)
        return Response(serializer.data)


class ChecklistItemsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ChecklistItems model with full CRUD operations.
    
    Available endpoints:
    - GET /api/checklist-items/ - List all checklist items
    - POST /api/checklist-items/ - Create new checklist item
    - GET /api/checklist-items/{id}/ - Retrieve specific checklist item
    - PUT /api/checklist-items/{id}/ - Update checklist item
    - PATCH /api/checklist-items/{id}/ - Partial update checklist item
    - DELETE /api/checklist-items/{id}/ - Delete checklist item
    """
    queryset = ChecklistItems.objects.all()
    serializer_class = ChecklistItemsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item_description']
    ordering_fields = ['item_id', 'sort_order']
    ordering = ['sort_order']

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Reorder checklist items based on provided order."""
        item_orders = request.data.get('item_orders', [])
        
        for item_order in item_orders:
            item_id = item_order.get('item_id')
            sort_order = item_order.get('sort_order')
            
            try:
                item = ChecklistItems.objects.get(item_id=item_id)
                item.sort_order = sort_order
                item.save()
            except ChecklistItems.DoesNotExist:
                continue
        
        return Response({'message': 'Items reordered successfully'}, status=status.HTTP_200_OK)


class InspectionReportsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for InspectionReports model with full CRUD operations.
    
    Available endpoints:
    - GET /api/inspection-reports/ - List all inspection reports
    - POST /api/inspection-reports/ - Create new inspection report
    - GET /api/inspection-reports/{id}/ - Retrieve specific inspection report
    - PUT /api/inspection-reports/{id}/ - Update inspection report
    - PATCH /api/inspection-reports/{id}/ - Partial update inspection report
    - DELETE /api/inspection-reports/{id}/ - Delete inspection report
    """
    queryset = InspectionReports.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['equipment', 'operator', 'supervisor', 'start_date', 'end_date']
    search_fields = ['report_number', 'equipment__serial_number', 'operator__full_name', 'supervisor__full_name']
    ordering_fields = ['report_id', 'report_number', 'start_date', 'end_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return different serializers for list and detail views."""
        if self.action == 'list':
            return InspectionReportsListSerializer
        return InspectionReportsSerializer

    @action(detail=False, methods=['get'])
    def current_week(self, request):
        """Get reports for current week."""
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        reports = self.queryset.filter(
            start_date__lte=end_of_week,
            end_date__gte=start_of_week
        )
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def daily_data(self, request, pk=None):
        """Get all daily inspection data for a specific report."""
        report = self.get_object()
        daily_data = DailyInspectionData.objects.filter(report=report)
        serializer = DailyInspectionDataSerializer(daily_data, many=True)
        return Response(serializer.data)


class DailyInspectionDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DailyInspectionData model with full CRUD operations.
    
    Available endpoints:
    - GET /api/daily-inspection-data/ - List all daily inspection data
    - POST /api/daily-inspection-data/ - Create new daily inspection data
    - GET /api/daily-inspection-data/{id}/ - Retrieve specific daily inspection data
    - PUT /api/daily-inspection-data/{id}/ - Update daily inspection data
    - PATCH /api/daily-inspection-data/{id}/ - Partial update daily inspection data
    - DELETE /api/daily-inspection-data/{id}/ - Delete daily inspection data
    """
    queryset = DailyInspectionData.objects.all()
    serializer_class = DailyInspectionDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report', 'item', 'status', 'inspection_date']
    search_fields = ['report__report_number', 'item__item_description']
    ordering_fields = ['inspection_data_id', 'inspection_date', 'status']
    ordering = ['-inspection_date', 'item__sort_order']

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple daily inspection data entries at once."""
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """Get daily inspection data within a date range."""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'Both start_date and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = self.queryset.filter(
            inspection_date__gte=start_date,
            inspection_date__lte=end_date
        )
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


class ReportNotesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ReportNotes model with full CRUD operations.
    
    Available endpoints:
    - GET /api/report-notes/ - List all report notes
    - POST /api/report-notes/ - Create new report note
    - GET /api/report-notes/{id}/ - Retrieve specific report note
    - PUT /api/report-notes/{id}/ - Update report note
    - PATCH /api/report-notes/{id}/ - Partial update report note
    - DELETE /api/report-notes/{id}/ - Delete report note
    """
    queryset = ReportNotes.objects.all()
    serializer_class = ReportNotesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report']
    search_fields = ['note_text', 'report__report_number']
    ordering_fields = ['note_id', 'created_at']
    ordering = ['-created_at']


class ReportAttachmentsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ReportAttachments model with full CRUD operations.
    
    Available endpoints:
    - GET /api/report-attachments/ - List all report attachments
    - POST /api/report-attachments/ - Create new report attachment
    - GET /api/report-attachments/{id}/ - Retrieve specific report attachment
    - PUT /api/report-attachments/{id}/ - Update report attachment
    - PATCH /api/report-attachments/{id}/ - Partial update report attachment
    - DELETE /api/report-attachments/{id}/ - Delete report attachment
    """
    queryset = ReportAttachments.objects.all()
    serializer_class = ReportAttachmentsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report']
    search_fields = ['caption', 'report__report_number']
    ordering_fields = ['attachment_id', 'uploaded_at']
    ordering = ['-uploaded_at']
