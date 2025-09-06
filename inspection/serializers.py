from rest_framework import serializers
from .models import (
    Equipment, Users, ChecklistItems, InspectionReports,
    DailyInspectionData, ReportNotes, ReportAttachments
)


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model with CRUD operations."""
    
    class Meta:
        model = Equipment
        fields = '__all__'
        read_only_fields = ['equipment_id']


class UsersSerializer(serializers.ModelSerializer):
    """Serializer for Users model with CRUD operations."""
    
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ['user_id']


class ChecklistItemsSerializer(serializers.ModelSerializer):
    """Serializer for ChecklistItems model with CRUD operations."""
    
    class Meta:
        model = ChecklistItems
        fields = '__all__'
        read_only_fields = ['item_id']


class ReportNotesSerializer(serializers.ModelSerializer):
    """Serializer for ReportNotes model."""
    
    class Meta:
        model = ReportNotes
        fields = '__all__'
        read_only_fields = ['note_id', 'created_at']


class ReportAttachmentsSerializer(serializers.ModelSerializer):
    """Serializer for ReportAttachments model."""
    
    class Meta:
        model = ReportAttachments
        fields = '__all__'
        read_only_fields = ['attachment_id', 'uploaded_at']


class DailyInspectionDataSerializer(serializers.ModelSerializer):
    """Serializer for DailyInspectionData model."""
    item_description = serializers.CharField(source='item.item_description', read_only=True)
    
    class Meta:
        model = DailyInspectionData
        fields = '__all__'
        read_only_fields = ['inspection_data_id']


class InspectionReportsSerializer(serializers.ModelSerializer):
    """Serializer for InspectionReports model with nested related data."""
    operator_name = serializers.CharField(source='operator.full_name', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.full_name', read_only=True)
    equipment_info = serializers.CharField(source='equipment.__str__', read_only=True)
    
    # Nested serializers for related data (optional - for detailed view)
    daily_inspection_data = DailyInspectionDataSerializer(many=True, read_only=True, source='dailyinspectiondata_set')
    report_notes = ReportNotesSerializer(many=True, read_only=True, source='reportnotes_set')
    report_attachments = ReportAttachmentsSerializer(many=True, read_only=True, source='reportattachments_set')
    
    class Meta:
        model = InspectionReports
        fields = '__all__'
        read_only_fields = ['report_id', 'created_at']


class InspectionReportsListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view of InspectionReports."""
    operator_name = serializers.CharField(source='operator.full_name', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.full_name', read_only=True)
    equipment_info = serializers.CharField(source='equipment.__str__', read_only=True)
    
    class Meta:
        model = InspectionReports
        fields = [
            'report_id', 'report_number', 'equipment', 'equipment_info',
            'operator', 'operator_name', 'supervisor', 'supervisor_name',
            'start_date', 'end_date', 'working_hours_from', 'working_hours_to',
            'created_at'
        ]
        read_only_fields = ['report_id', 'created_at']