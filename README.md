# Daily Equipment Inspection System - Django Models

This Django application implements a comprehensive database schema for a Daily Equipment Inspection System, designed to digitize equipment inspection forms.

## Models Overview

### 1. Equipment
- **Purpose**: Central registry of all machinery
- **Key Fields**: 
  - `serial_number`: Unique equipment identifier (الرقم التسلسلي)
  - `equipment_type`: Type of equipment (نوع المعدة)
  - `model`: Specific model
  - `status`: Current status (Active, Under Maintenance, Decommissioned)

### 2. Users
- **Purpose**: Manage operators and supervisors
- **Key Fields**:
  - `full_name`: Person's name (سائق المعدة / المهندس المشرف)
  - `role`: User role (Operator, Supervisor, Admin)
  - `employee_number`: Official employee number

### 3. ChecklistItems
- **Purpose**: Flexible checklist system for inspection items
- **Key Fields**:
  - `item_description`: Description of inspection item (e.g., "مستوى زيت المحرك")
  - `sort_order`: Display order on forms

### 4. InspectionReports
- **Purpose**: Main table for weekly inspection forms
- **Key Fields**:
  - `report_number`: Form number (الرقم)
  - `start_date`: Week start date (من تاريخ)
  - `end_date`: Week end date (الى تاريخ)
  - `working_hours_from/to`: Work hours (ساعات العمل)

### 5. DailyInspectionData
- **Purpose**: Store daily check results
- **Key Fields**:
  - `inspection_date`: Specific check date
  - `status`: Check result (Good/Not Good)

### 6. ReportNotes
- **Purpose**: Free-text observations
- **Key Fields**:
  - `note_text`: Observation content (الملاحظات إن وجدت)

### 7. ReportAttachments
- **Purpose**: Manage attached files and photos
- **Key Fields**:
  - `file_path`: File storage path
  - `caption`: Optional file description

## Features

- **Flexible Design**: Checklist items can be modified without changing database structure
- **Bilingual Support**: Arabic and English field descriptions
- **Complete Audit Trail**: Timestamps and relationships maintain data integrity
- **File Management**: Support for photo and document attachments
- **Admin Interface**: Full Django admin configuration for easy management

## Database Setup

1. Install Django and dependencies
2. Add 'inspection' to INSTALLED_APPS in settings.py
3. Run migrations:
   ```bash
   python manage.py makemigrations inspection
   python manage.py migrate
   ```
4. Load initial checklist items:
   ```bash
   python manage.py load_checklist_items
   ```

## Admin Interface

Access the Django admin interface to:
- Manage equipment inventory
- Configure users and roles
- Customize checklist items
- View and manage inspection reports
- Access daily inspection data with filtering and search

## Relationships

- Equipment → Many InspectionReports
- Users → Many InspectionReports (as operator or supervisor)
- InspectionReports → Many DailyInspectionData, ReportNotes, ReportAttachments
- ChecklistItems → Many DailyInspectionData

The schema maintains referential integrity while providing flexibility for future enhancements.