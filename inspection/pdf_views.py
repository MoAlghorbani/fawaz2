from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from wkhtmltopdf.views import PDFTemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from datetime import datetime, timedelta
from .models import InspectionReports, DailyInspectionData, ChecklistItems


class InspectionReportPDFView(PDFTemplateView):
    """
    Generate PDF report for inspection reports
    """
    template_name = 'inspection/inspection_report.html'
    filename = 'inspection_report.pdf'
    
    cmd_options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',  
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': 'UTF-8',
        'orientation': 'Portrait',
        'no-outline': None,
        'enable-local-file-access': None,
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the report
        report_id = self.kwargs.get('report_id')
        report = get_object_or_404(InspectionReports, report_id=report_id)
        
        # Get all checklist items ordered by sort_order
        checklist_items = ChecklistItems.objects.all().order_by('sort_order')
        
        # Create date range for the week
        current_date = report.start_date
        dates = []
        while current_date <= report.end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Get daily inspection data organized by item and date
        daily_data = DailyInspectionData.objects.filter(report=report)
        
        # Create a matrix of inspection data
        inspection_matrix = {}
        for item in checklist_items:
            inspection_matrix[item.item_id] = {}
            for date in dates:
                # Find the inspection data for this item and date
                try:
                    data = daily_data.get(item=item, inspection_date=date)
                    inspection_matrix[item.item_id][date] = data.status
                except DailyInspectionData.DoesNotExist:
                    inspection_matrix[item.item_id][date] = None
        
        # Get notes and attachments
        notes = report.reportnotes_set.all().order_by('created_at')
        attachments = report.reportattachments_set.all().order_by('uploaded_at')
        
        context.update({
            'report': report,
            'checklist_items': checklist_items,
            'dates': dates,
            'inspection_matrix': inspection_matrix,
            'notes': notes,
            'attachments': attachments,
            'date_headers': [date.strftime('%A\n%d/%m') for date in dates],
            'generated_at': datetime.now(),
        })
        
        return context
    
    def get_filename(self):
        report_id = self.kwargs.get('report_id')
        report = get_object_or_404(InspectionReports, report_id=report_id)
        return f'inspection_report_{report.report_number}_{report.start_date}.pdf'


@extend_schema(
    summary='Generate PDF Report',
    description='Generate a PDF report for a specific inspection report.',
    tags=['Reports'],
    responses={
        200: {
            'description': 'PDF file',
            'content': {
                'application/pdf': {
                    'schema': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        404: {
            'description': 'Report not found',
            'example': {'error': 'Report not found'}
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_inspection_report_pdf(request, report_id):
    """
    API endpoint to generate PDF report
    """
    try:
        # Check if report exists
        report = get_object_or_404(InspectionReports, report_id=report_id)
        
        # Create PDF view instance
        pdf_view = InspectionReportPDFView()
        pdf_view.kwargs = {'report_id': report_id}
        pdf_view.request = request
        
        # Generate PDF
        response = pdf_view.get(request, report_id=report_id)
        
        return response
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate PDF: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary='Get Report Data for PDF Preview',
    description='Get structured report data that would be used for PDF generation.',
    tags=['Reports'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_pdf_data(request, report_id):
    """
    API endpoint to get report data structure for PDF preview
    """
    try:
        report = get_object_or_404(InspectionReports, report_id=report_id)
        
        # Get all checklist items
        checklist_items = ChecklistItems.objects.all().order_by('sort_order')
        
        # Create date range
        current_date = report.start_date
        dates = []
        while current_date <= report.end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Get daily inspection data
        daily_data = DailyInspectionData.objects.filter(report=report)
        
        # Create inspection matrix
        inspection_matrix = []
        for item in checklist_items:
            item_data = {
                'item_id': item.item_id,
                'description': item.item_description,
                'sort_order': item.sort_order,
                'daily_status': {}
            }
            
            for date in dates:
                try:
                    data = daily_data.get(item=item, inspection_date=date)
                    item_data['daily_status'][date.isoformat()] = data.status
                except DailyInspectionData.DoesNotExist:
                    item_data['daily_status'][date.isoformat()] = None
            
            inspection_matrix.append(item_data)
        
        # Get notes and attachments
        notes = list(report.reportnotes_set.values('note_text', 'created_at'))
        attachments = list(report.reportattachments_set.values('file_path', 'caption', 'uploaded_at'))
        
        response_data = {
            'report': {
                'report_id': report.report_id,
                'report_number': report.report_number,
                'equipment': {
                    'id': report.equipment.equipment_id,
                    'serial_number': report.equipment.serial_number,
                    'type': report.equipment.equipment_type,
                    'model': report.equipment.model,
                },
                'operator': {
                    'id': report.operator.user_id,
                    'name': report.operator.full_name,
                    'employee_number': report.operator.employee_number,
                },
                'supervisor': {
                    'id': report.supervisor.user_id,
                    'name': report.supervisor.full_name,
                    'employee_number': report.supervisor.employee_number,
                },
                'start_date': report.start_date,
                'end_date': report.end_date,
                'working_hours_from': report.working_hours_from,
                'working_hours_to': report.working_hours_to,
                'created_at': report.created_at,
            },
            'dates': [date.isoformat() for date in dates],
            'inspection_matrix': inspection_matrix,
            'notes': notes,
            'attachments': attachments,
            'summary': {
                'total_checklist_items': len(checklist_items),
                'total_inspection_days': len(dates),
                'total_notes': len(notes),
                'total_attachments': len(attachments),
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to get report data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )