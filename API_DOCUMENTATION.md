# Daily Equipment Inspection System - API Documentation

## Overview

This Django REST API provides complete CRUD operations for all models in the Daily Equipment Inspection System. The API is designed to support mobile and web applications for managing equipment inspections.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication

The API uses Django's built-in authentication. You need to be logged in to access most endpoints.

- **Login URL**: `http://127.0.0.1:8000/api-auth/login/`
- **Logout URL**: `http://127.0.0.1:8000/api-auth/logout/`

## API Endpoints

### 1. Equipment Management
**Base URL**: `/api/equipment/`

#### Available Operations:
- `GET /api/equipment/` - List all equipment
- `POST /api/equipment/` - Create new equipment
- `GET /api/equipment/{id}/` - Retrieve specific equipment
- `PUT /api/equipment/{id}/` - Update equipment
- `PATCH /api/equipment/{id}/` - Partial update equipment
- `DELETE /api/equipment/{id}/` - Delete equipment

#### Custom Actions:
- `GET /api/equipment/active/` - Get only active equipment

#### Filters:
- `status` - Filter by equipment status
- `equipment_type` - Filter by equipment type

#### Search:
- Search in: `serial_number`, `equipment_type`, `model`

#### Example Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/equipment/" \
     -H "Authorization: Basic <credentials>"
```

### 2. Users Management
**Base URL**: `/api/users/`

#### Available Operations:
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Retrieve specific user
- `PUT /api/users/{id}/` - Update user
- `PATCH /api/users/{id}/` - Partial update user
- `DELETE /api/users/{id}/` - Delete user

#### Custom Actions:
- `GET /api/users/operators/` - Get only operators
- `GET /api/users/supervisors/` - Get only supervisors

#### Filters:
- `role` - Filter by user role

#### Search:
- Search in: `full_name`, `employee_number`

### 3. Checklist Items Management
**Base URL**: `/api/checklist-items/`

#### Available Operations:
- `GET /api/checklist-items/` - List all checklist items
- `POST /api/checklist-items/` - Create new checklist item
- `GET /api/checklist-items/{id}/` - Retrieve specific checklist item
- `PUT /api/checklist-items/{id}/` - Update checklist item
- `PATCH /api/checklist-items/{id}/` - Partial update checklist item
- `DELETE /api/checklist-items/{id}/` - Delete checklist item

#### Custom Actions:
- `POST /api/checklist-items/reorder/` - Reorder checklist items

#### Search:
- Search in: `item_description`

#### Example Reorder Request:
```bash
curl -X POST "http://127.0.0.1:8000/api/checklist-items/reorder/" \
     -H "Content-Type: application/json" \
     -d '{
       "item_orders": [
         {"item_id": 1, "sort_order": 1},
         {"item_id": 2, "sort_order": 2}
       ]
     }'
```

### 4. Inspection Reports Management
**Base URL**: `/api/inspection-reports/`

#### Available Operations:
- `GET /api/inspection-reports/` - List all inspection reports
- `POST /api/inspection-reports/` - Create new inspection report
- `GET /api/inspection-reports/{id}/` - Retrieve specific inspection report
- `PUT /api/inspection-reports/{id}/` - Update inspection report
- `PATCH /api/inspection-reports/{id}/` - Partial update inspection report
- `DELETE /api/inspection-reports/{id}/` - Delete inspection report

#### Custom Actions:
- `GET /api/inspection-reports/current_week/` - Get reports for current week
- `GET /api/inspection-reports/{id}/daily_data/` - Get daily inspection data for specific report

#### Filters:
- `equipment` - Filter by equipment ID
- `operator` - Filter by operator ID
- `supervisor` - Filter by supervisor ID
- `start_date` - Filter by start date
- `end_date` - Filter by end date

#### Search:
- Search in: `report_number`, `equipment__serial_number`, `operator__full_name`, `supervisor__full_name`

### 5. Daily Inspection Data Management
**Base URL**: `/api/daily-inspection-data/`

#### Available Operations:
- `GET /api/daily-inspection-data/` - List all daily inspection data
- `POST /api/daily-inspection-data/` - Create new daily inspection data
- `GET /api/daily-inspection-data/{id}/` - Retrieve specific daily inspection data
- `PUT /api/daily-inspection-data/{id}/` - Update daily inspection data
- `PATCH /api/daily-inspection-data/{id}/` - Partial update daily inspection data
- `DELETE /api/daily-inspection-data/{id}/` - Delete daily inspection data

#### Custom Actions:
- `POST /api/daily-inspection-data/bulk_create/` - Create multiple entries at once
- `GET /api/daily-inspection-data/by_date_range/` - Get data within date range

#### Filters:
- `report` - Filter by report ID
- `item` - Filter by checklist item ID
- `status` - Filter by inspection status
- `inspection_date` - Filter by inspection date

#### Search:
- Search in: `report__report_number`, `item__item_description`

#### Example Bulk Create:
```bash
curl -X POST "http://127.0.0.1:8000/api/daily-inspection-data/bulk_create/" \
     -H "Content-Type: application/json" \
     -d '[
       {
         "report": 1,
         "item": 1,
         "inspection_date": "2025-08-30",
         "status": "good"
       },
       {
         "report": 1,
         "item": 2,
         "inspection_date": "2025-08-30",
         "status": "not_good"
       }
     ]'
```

#### Example Date Range Query:
```bash
curl -X GET "http://127.0.0.1:8000/api/daily-inspection-data/by_date_range/?start_date=2025-08-01&end_date=2025-08-31"
```

### 6. Report Notes Management
**Base URL**: `/api/report-notes/`

#### Available Operations:
- `GET /api/report-notes/` - List all report notes
- `POST /api/report-notes/` - Create new report note
- `GET /api/report-notes/{id}/` - Retrieve specific report note
- `PUT /api/report-notes/{id}/` - Update report note
- `PATCH /api/report-notes/{id}/` - Partial update report note
- `DELETE /api/report-notes/{id}/` - Delete report note

#### Filters:
- `report` - Filter by report ID

#### Search:
- Search in: `note_text`, `report__report_number`

### 7. Report Attachments Management
**Base URL**: `/api/report-attachments/`

#### Available Operations:
- `GET /api/report-attachments/` - List all report attachments
- `POST /api/report-attachments/` - Create new report attachment
- `GET /api/report-attachments/{id}/` - Retrieve specific report attachment
- `PUT /api/report-attachments/{id}/` - Update report attachment
- `PATCH /api/report-attachments/{id}/` - Partial update report attachment
- `DELETE /api/report-attachments/{id}/` - Delete report attachment

#### Filters:
- `report` - Filter by report ID

#### Search:
- Search in: `caption`, `report__report_number`

## Response Format

### Success Response Format:
```json
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/equipment/?page=2",
  "previous": null,
  "results": [
    {
      "equipment_id": 1,
      "serial_number": "EQ-001",
      "equipment_type": "Excavator",
      "model": "CAT 320",
      "status": "active"
    }
  ]
}
```

### Error Response Format:
```json
{
  "field_name": ["Error message for this field"],
  "non_field_errors": ["General error message"]
}
```

## Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Pagination

All list endpoints support pagination with 20 items per page by default.

Query parameters:
- `page` - Page number
- `page_size` - Number of items per page (max 100)

## Common Query Parameters

- `search` - Search across specified fields
- `ordering` - Order results (prefix with `-` for descending)
- Various filter parameters specific to each endpoint

## Example Usage Scenarios

### 1. Create a Weekly Inspection Report
```bash
# First, create the inspection report
curl -X POST "http://127.0.0.1:8000/api/inspection-reports/" \
     -H "Content-Type: application/json" \
     -d '{
       "report_number": "RPT-001",
       "equipment": 1,
       "operator": 1,
       "supervisor": 2,
       "start_date": "2025-08-26",
       "end_date": "2025-09-01",
       "working_hours_from": "08:00:00",
       "working_hours_to": "17:00:00"
     }'

# Then, create daily inspection data for each day
curl -X POST "http://127.0.0.1:8000/api/daily-inspection-data/bulk_create/" \
     -H "Content-Type: application/json" \
     -d '[
       {
         "report": 1,
         "item": 1,
         "inspection_date": "2025-08-26",
         "status": "good"
       }
     ]'
```

### 2. Get All Data for a Specific Report
```bash
curl -X GET "http://127.0.0.1:8000/api/inspection-reports/1/"
```

This will return the report with all nested data including daily inspection data, notes, and attachments.

## Notes

- All timestamps are in UTC
- File uploads for attachments should use `multipart/form-data`
- The API supports both JSON and form data for most endpoints
- Filtering and searching are case-insensitive