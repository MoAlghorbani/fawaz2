from django.contrib import admin
from .models import (
    Equipment, Users, ChecklistItems, InspectionReports,
    DailyInspectionData, ReportNotes, ReportAttachments
)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_id', 'serial_number', 'equipment_type', 'model', 'status']
    list_filter = ['status', 'equipment_type']
    search_fields = ['serial_number', 'equipment_type', 'model']
    ordering = ['equipment_type', 'serial_number']


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'full_name', 'role', 'employee_number']
    list_filter = ['role']
    search_fields = ['full_name', 'employee_number']
    ordering = ['full_name']


@admin.register(ChecklistItems)
class ChecklistItemsAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'sort_order', 'item_description']
    list_editable = ['sort_order']
    ordering = ['sort_order']


class DailyInspectionDataInline(admin.TabularInline):
    model = DailyInspectionData
    extra = 0
    readonly_fields = ['inspection_data_id']


class ReportNotesInline(admin.TabularInline):
    model = ReportNotes
    extra = 0
    readonly_fields = ['note_id', 'created_at']


class ReportAttachmentsInline(admin.TabularInline):
    model = ReportAttachments
    extra = 0
    readonly_fields = ['attachment_id', 'uploaded_at']


@admin.register(InspectionReports)
class InspectionReportsAdmin(admin.ModelAdmin):
    list_display = ['report_id', 'report_number', 'equipment', 'operator', 'supervisor', 'start_date', 'end_date', 'created_at']
    list_filter = ['start_date', 'end_date', 'equipment__equipment_type', 'created_at']
    search_fields = ['report_number', 'equipment__serial_number', 'operator__full_name', 'supervisor__full_name']
    date_hierarchy = 'start_date'
    ordering = ['-created_at']
    inlines = [DailyInspectionDataInline, ReportNotesInline, ReportAttachmentsInline]
    
    fieldsets = (
        ('Report Information', {
            'fields': ('report_number', 'equipment')
        }),
        ('Personnel', {
            'fields': ('operator', 'supervisor')
        }),
        ('Time Period', {
            'fields': ('start_date', 'end_date', 'working_hours_from', 'working_hours_to')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']


@admin.register(DailyInspectionData)
class DailyInspectionDataAdmin(admin.ModelAdmin):
    list_display = ['inspection_data_id', 'report', 'item', 'inspection_date', 'status']
    list_filter = ['status', 'inspection_date', 'report__equipment__equipment_type']
    search_fields = ['report__report_number', 'item__item_description']
    date_hierarchy = 'inspection_date'
    ordering = ['-inspection_date', 'item__sort_order']


@admin.register(ReportNotes)
class ReportNotesAdmin(admin.ModelAdmin):
    list_display = ['note_id', 'report', 'note_text_preview', 'created_at']
    list_filter = ['created_at', 'report__equipment__equipment_type']
    search_fields = ['report__report_number', 'note_text']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def note_text_preview(self, obj):
        return obj.note_text[:100] + '...' if len(obj.note_text) > 100 else obj.note_text
    note_text_preview.short_description = 'Note Preview'


@admin.register(ReportAttachments)
class ReportAttachmentsAdmin(admin.ModelAdmin):
    list_display = ['attachment_id', 'report', 'file_name', 'caption', 'uploaded_at']
    list_filter = ['uploaded_at', 'report__equipment__equipment_type']
    search_fields = ['report__report_number', 'caption']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    
    def file_name(self, obj):
        return obj.file_path.name.split('/')[-1] if obj.file_path.name else 'No file'
    file_name.short_description = 'File Name'
