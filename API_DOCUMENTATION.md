# Daily Equipment Inspection System - API Documentation

## Overview

This Django REST API provides complete CRUD operations for all models in the Daily Equipment Inspection System. The API is designed to support mobile and web applications for managing equipment inspections.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication

The API uses token-based authentication for better security and API client integration.

- **Login URL**: `http://127.0.0.1:8000/api/auth/login/`
- **Logout URL**: `http://127.0.0.1:8000/api/auth/logout/`
- **User Info URL**: `http://127.0.0.1:8000/api/auth/user/`

### How Token Authentication Works

1. **Login** with username/password to get a token
2. **Include the token** in the `Authorization` header for all subsequent requests
3. **Logout** to delete the token (optional, tokens don't expire by default)

### Authentication Header Format
```
Authorization: Token your-token-here
```

### Authentication Endpoints

#### Login
**POST** `/api/auth/login/`

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (Success - 200):**
```json
{
  "message": "Login successful",
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": "",
    "is_staff": true,
    "is_superuser": true
  }
}
```

**Response (Error - 401):**
```json
{
  "error": "Invalid username or password"
}
```

#### Logout
**POST** `/api/auth/logout/`

**Headers Required:**
```
Authorization: Token your-token-here
```

**Request Body:** None required

**Response (200):**
```json
{
  "message": "Logout successful"
}
```

#### Get User Info
**GET** `/api/auth/user/`

**Headers Required:**
```
Authorization: Token your-token-here
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": "",
    "is_staff": true,
    "is_superuser": true
  }
}
```

### Example Usage with Token

**Step 1: Login to get token**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "admin123"
     }'
```

**Step 2: Use token for API requests**
```bash
curl -X GET "http://127.0.0.1:8000/api/equipment/" \
     -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

**Step 3: Logout (optional)**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/logout/" \
     -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

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

#### Request Body Examples:

**Create Equipment (POST):**
```json
{
  "serial_number": "EQ-001",
  "equipment_type": "Excavator",
  "model": "CAT 320",
  "status": "active"
}
```

**Update Equipment (PUT):**
```json
{
  "serial_number": "EQ-001",
  "equipment_type": "Excavator",
  "model": "CAT 320D",
  "status": "active"
}
```

**Partial Update Equipment (PATCH):**
```json
{
  "status": "maintenance"
}
```

#### Response Examples:

**Equipment Object:**
```json
{
  "equipment_id": 1,
  "serial_number": "EQ-001",
  "equipment_type": "Excavator",
  "model": "CAT 320",
  "status": "active"
}
```

#### Custom Actions:
- `GET /api/equipment/active/` - Get only active equipment

#### Filters:
- `status` - Filter by equipment status (`active`, `maintenance`, `decommissioned`)
- `equipment_type` - Filter by equipment type

#### Search:
- Search in: `serial_number`, `equipment_type`, `model`

#### Example Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/equipment/?status=active&search=CAT" \
     -H "Content-Type: application/json" \
     -H "Authorization: Token your-token-here"
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

#### Request Body Examples:

**Create User (POST):**
```json
{
  "full_name": "Ahmed Ali",
  "role": "operator",
  "employee_number": "EMP-001"
}
```

**Update User (PUT):**
```json
{
  "full_name": "Ahmed Ali Mohamed",
  "role": "supervisor",
  "employee_number": "EMP-001"
}
```

**Partial Update User (PATCH):**
```json
{
  "role": "supervisor"
}
```

#### Response Examples:

**User Object:**
```json
{
  "user_id": 1,
  "full_name": "Ahmed Ali",
  "role": "operator",
  "employee_number": "EMP-001"
}
```

#### Custom Actions:
- `GET /api/users/operators/` - Get only operators
- `GET /api/users/supervisors/` - Get only supervisors

#### Filters:
- `role` - Filter by user role (`operator`, `supervisor`, `admin`)

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

#### Request Body Examples:

**Create Checklist Item (POST):**
```json
{
  "item_description": "مستوى زيت المحرك (Engine oil level)",
  "sort_order": 1
}
```

**Update Checklist Item (PUT):**
```json
{
  "item_description": "مستوى زيت المحرك والفلتر (Engine oil and filter level)",
  "sort_order": 1
}
```

**Partial Update Checklist Item (PATCH):**
```json
{
  "sort_order": 5
}
```

#### Response Examples:

**Checklist Item Object:**
```json
{
  "item_id": 1,
  "item_description": "مستوى زيت المحرك (Engine oil level)",
  "sort_order": 1
}
```

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
         {"item_id": 2, "sort_order": 2},
         {"item_id": 3, "sort_order": 3}
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

#### Request Body Examples:

**Create Inspection Report (POST):**
```json
{
  "report_number": "RPT-001",
  "equipment": 1,
  "operator": 1,
  "supervisor": 2,
  "start_date": "2025-09-02",
  "end_date": "2025-09-08",
  "working_hours_from": "08:00:00",
  "working_hours_to": "17:00:00"
}
```

**Update Inspection Report (PUT):**
```json
{
  "report_number": "RPT-001-UPDATED",
  "equipment": 1,
  "operator": 1,
  "supervisor": 3,
  "start_date": "2025-09-02",
  "end_date": "2025-09-08",
  "working_hours_from": "07:00:00",
  "working_hours_to": "16:00:00"
}
```

**Partial Update Inspection Report (PATCH):**
```json
{
  "supervisor": 3,
  "working_hours_from": "07:30:00"
}
```

#### Response Examples:

**Inspection Report Object (List View):**
```json
{
  "report_id": 1,
  "report_number": "RPT-001",
  "equipment": 1,
  "equipment_info": "Excavator - EQ-001",
  "operator": 1,
  "operator_name": "Ahmed Ali",
  "supervisor": 2,
  "supervisor_name": "Mohamed Hassan",
  "start_date": "2025-09-02",
  "end_date": "2025-09-08",
  "working_hours_from": "08:00:00",
  "working_hours_to": "17:00:00",
  "created_at": "2025-09-06T20:40:04.123456Z"
}
```

**Inspection Report Object (Detail View with Nested Data):**
```json
{
  "report_id": 1,
  "report_number": "RPT-001",
  "equipment": 1,
  "equipment_info": "Excavator - EQ-001",
  "operator": 1,
  "operator_name": "Ahmed Ali",
  "supervisor": 2,
  "supervisor_name": "Mohamed Hassan",
  "start_date": "2025-09-02",
  "end_date": "2025-09-08",
  "working_hours_from": "08:00:00",
  "working_hours_to": "17:00:00",
  "created_at": "2025-09-06T20:40:04.123456Z",
  "daily_inspection_data": [
    {
      "inspection_data_id": 1,
      "item": 1,
      "item_description": "مستوى زيت المحرك (Engine oil level)",
      "inspection_date": "2025-09-02",
      "status": "good"
    }
  ],
  "report_notes": [
    {
      "note_id": 1,
      "note_text": "Equipment running smoothly",
      "created_at": "2025-09-06T20:40:04.123456Z"
    }
  ],
  "report_attachments": [
    {
      "attachment_id": 1,
      "file_path": "/media/inspection_attachments/2025/09/06/photo.jpg",
      "caption": "Engine bay photo",
      "uploaded_at": "2025-09-06T20:40:04.123456Z"
    }
  ]
}
```

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

#### Request Body Examples:

**Create Daily Inspection Data (POST):**
```json
{
  "report": 1,
  "item": 1,
  "inspection_date": "2025-09-06",
  "status": "good"
}
```

**Update Daily Inspection Data (PUT):**
```json
{
  "report": 1,
  "item": 1,
  "inspection_date": "2025-09-06",
  "status": "not_good"
}
```

**Partial Update Daily Inspection Data (PATCH):**
```json
{
  "status": "not_good"
}
```

#### Response Examples:

**Daily Inspection Data Object:**
```json
{
  "inspection_data_id": 1,
  "report": 1,
  "item": 1,
  "item_description": "مستوى زيت المحرك (Engine oil level)",
  "inspection_date": "2025-09-06",
  "status": "good"
}
```

#### Custom Actions:
- `POST /api/daily-inspection-data/bulk_create/` - Create multiple entries at once
- `GET /api/daily-inspection-data/by_date_range/` - Get data within date range

#### Filters:
- `report` - Filter by report ID
- `item` - Filter by checklist item ID
- `status` - Filter by inspection status (`good`, `not_good`)
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
         "inspection_date": "2025-09-06",
         "status": "good"
       },
       {
         "report": 1,
         "item": 2,
         "inspection_date": "2025-09-06",
         "status": "not_good"
       },
       {
         "report": 1,
         "item": 3,
         "inspection_date": "2025-09-06",
         "status": "good"
       }
     ]'
```

#### Example Date Range Query:
```bash
curl -X GET "http://127.0.0.1:8000/api/daily-inspection-data/by_date_range/?start_date=2025-09-01&end_date=2025-09-30"
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

#### Request Body Examples:

**Create Report Note (POST):**
```json
{
  "report": 1,
  "note_text": "Equipment shows signs of wear on the hydraulic cylinder. Recommend inspection by maintenance team."
}
```

**Update Report Note (PUT):**
```json
{
  "report": 1,
  "note_text": "Equipment shows signs of wear on the hydraulic cylinder. Maintenance team notified and repair scheduled for next week."
}
```

**Partial Update Report Note (PATCH):**
```json
{
  "note_text": "Hydraulic cylinder repaired successfully. Equipment back to normal operation."
}
```

#### Response Examples:

**Report Note Object:**
```json
{
  "note_id": 1,
  "report": 1,
  "note_text": "Equipment shows signs of wear on the hydraulic cylinder. Recommend inspection by maintenance team.",
  "created_at": "2025-09-06T20:40:04.123456Z"
}
```

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

#### Request Body Examples:

**Create Report Attachment (POST) - Form Data:**
```bash
# Using curl with form data for file upload
curl -X POST "http://127.0.0.1:8000/api/report-attachments/" \
     -H "Content-Type: multipart/form-data" \
     -F "report=1" \
     -F "file_path=@/path/to/image.jpg" \
     -F "caption=Engine bay inspection photo"
```

**Create Report Attachment (POST) - JSON (without file):**
```json
{
  "report": 1,
  "caption": "External inspection photo"
}
```

**Update Report Attachment (PUT):**
```json
{
  "report": 1,
  "caption": "Updated: Engine bay inspection photo - showing hydraulic leak"
}
```

**Partial Update Report Attachment (PATCH):**
```json
{
  "caption": "Hydraulic leak fixed - follow-up photo"
}
```

#### Response Examples:

**Report Attachment Object:**
```json
{
  "attachment_id": 1,
  "report": 1,
  "file_path": "/media/inspection_attachments/2025/09/06/engine_bay_photo.jpg",
  "caption": "Engine bay inspection photo",
  "uploaded_at": "2025-09-06T20:40:04.123456Z"
}
```

#### Filters:
- `report` - Filter by report ID

#### Search:
- Search in: `caption`, `report__report_number`

#### File Upload Notes:
- Use `multipart/form-data` content type for file uploads
- Supported file types: Images (JPG, PNG, GIF), Documents (PDF, DOC, DOCX)
- Maximum file size: 10MB (configurable)
- Files are stored in `/media/inspection_attachments/YYYY/MM/DD/` directory structure

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

### 1. Complete Workflow: Create a Weekly Inspection Report with Daily Data

**Step 1: Create the Inspection Report**
```bash
curl -X POST "http://127.0.0.1:8000/api/inspection-reports/" \
     -H "Content-Type: application/json" \
     -d '{
       "report_number": "RPT-001",
       "equipment": 1,
       "operator": 1,
       "supervisor": 2,
       "start_date": "2025-09-02",
       "end_date": "2025-09-08",
       "working_hours_from": "08:00:00",
       "working_hours_to": "17:00:00"
     }'
```

**Step 2: Add Daily Inspection Data (Bulk Create)**
```bash
curl -X POST "http://127.0.0.1:8000/api/daily-inspection-data/bulk_create/" \
     -H "Content-Type: application/json" \
     -d '[
       {
         "report": 1,
         "item": 1,
         "inspection_date": "2025-09-02",
         "status": "good"
       },
       {
         "report": 1,
         "item": 2,
         "inspection_date": "2025-09-02",
         "status": "good"
       },
       {
         "report": 1,
         "item": 3,
         "inspection_date": "2025-09-02",
         "status": "not_good"
       }
     ]'
```

**Step 3: Add Notes for Issues**
```bash
curl -X POST "http://127.0.0.1:8000/api/report-notes/" \
     -H "Content-Type: application/json" \
     -d '{
       "report": 1,
       "note_text": "Tire pressure low on front left wheel. Needs attention before next shift."
     }'
```

**Step 4: Add Photo Attachment**
```bash
curl -X POST "http://127.0.0.1:8000/api/report-attachments/" \
     -H "Content-Type: multipart/form-data" \
     -F "report=1" \
     -F "file_path=@tire_inspection.jpg" \
     -F "caption=Front left tire showing low pressure"
```

### 2. Get All Data for a Specific Report
```bash
curl -X GET "http://127.0.0.1:8000/api/inspection-reports/1/"
```

This will return the complete report with all nested data including daily inspection data, notes, and attachments.

### 3. Search and Filter Examples

**Find all active excavators:**
```bash
curl -X GET "http://127.0.0.1:8000/api/equipment/?status=active&equipment_type=Excavator"
```

**Find all reports for a specific operator:**
```bash
curl -X GET "http://127.0.0.1:8000/api/inspection-reports/?operator=1"
```

**Find all daily data with issues in date range:**
```bash
curl -X GET "http://127.0.0.1:8000/api/daily-inspection-data/by_date_range/?start_date=2025-09-01&end_date=2025-09-30&status=not_good"
```

**Search for reports by equipment serial number:**
```bash
curl -X GET "http://127.0.0.1:8000/api/inspection-reports/?search=EQ-001"
```

## Notes

- All timestamps are in UTC format
- File uploads for attachments must use `multipart/form-data` content type
- The API supports both JSON and form data for most endpoints (except file uploads)
- All filtering and searching are case-insensitive
- Date fields should be in YYYY-MM-DD format
- Time fields should be in HH:MM:SS format
- Status fields have predefined choices:
  - Equipment status: `active`, `maintenance`, `decommissioned`
  - User roles: `operator`, `supervisor`, `admin`  
  - Inspection status: `good`, `not_good`
- Foreign key relationships require valid IDs from related models
- Bulk operations are available for daily inspection data to improve performance
- All endpoints support standard REST conventions with appropriate HTTP methods