from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    Daily Equipment Inspection System API Root
    
    This API provides CRUD operations for all inspection system models.
    """
    return Response({
        'equipment': reverse('equipment-list', request=request, format=format),
        'users': reverse('users-list', request=request, format=format),
        'checklist-items': reverse('checklist-items-list', request=request, format=format),
        'inspection-reports': reverse('inspection-reports-list', request=request, format=format),
        'daily-inspection-data': reverse('daily-inspection-data-list', request=request, format=format),
        'report-notes': reverse('report-notes-list', request=request, format=format),
        'report-attachments': reverse('report-attachments-list', request=request, format=format),
        'api-auth': reverse('rest_framework:login', request=request, format=format),
        'admin': request.build_absolute_uri('/admin/'),
    })