from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Equipment(models.Model):
    """Table to store information about each piece of equipment."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('decommissioned', 'Decommissioned'),
    ]
    
    equipment_id = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=100, unique=True, help_text="Equipment's serial number (الرقم التسلسلي)")
    equipment_type = models.CharField(max_length=100, help_text="Type of equipment (نوع المعدة), e.g., Excavator, Bulldozer")
    model = models.CharField(max_length=100, help_text="Specific model of the equipment")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    class Meta:
        db_table = 'equipment'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
    
    def __str__(self):
        return f"{self.equipment_type} - {self.serial_number}"


class Users(models.Model):
    """Table to hold information about personnel (operators and supervisors)."""
    
    ROLE_CHOICES = [
        ('operator', 'Operator'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Admin'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200, help_text="Name of the person (سائق المعدة / المهندس المشرف)")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    employee_number = models.CharField(max_length=50, unique=True, help_text="Official employee number")
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.full_name} ({self.role})"


class ChecklistItems(models.Model):
    """Table to store the list of items to be checked, making the system flexible."""
    
    item_id = models.AutoField(primary_key=True)
    item_description = models.TextField(help_text="Text of the item, e.g., 'مستوى زيت المحرك' (Engine oil level)")
    sort_order = models.IntegerField(help_text="Number to control the order in which items appear on the form")
    
    class Meta:
        db_table = 'checklist_items'
        verbose_name = 'Checklist Item'
        verbose_name_plural = 'Checklist Items'
        ordering = ['sort_order']
    
    def __str__(self):
        return f"{self.sort_order}. {self.item_description}"


class InspectionReports(models.Model):
    """Main table that represents a single, completed form for one week."""
    
    report_id = models.AutoField(primary_key=True)
    report_number = models.CharField(max_length=50, help_text="Form's number (الرقم)")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, help_text="Equipment being inspected")
    operator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='operator_reports', help_text="Driver of the equipment")
    supervisor = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='supervisor_reports', help_text="Engineer supervisor")
    start_date = models.DateField(help_text="Start of the inspection week (من تاريخ)")
    end_date = models.DateField(help_text="End of the inspection week (الى تاريخ)")
    working_hours_from = models.TimeField(help_text="Start of work hours (ساعات العمل من)")
    working_hours_to = models.TimeField(help_text="End of work hours (الى ساعة)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp for when the report was created")
    
    class Meta:
        db_table = 'inspection_reports'
        verbose_name = 'Inspection Report'
        verbose_name_plural = 'Inspection Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report {self.report_number} - {self.equipment} ({self.start_date} to {self.end_date})"


class DailyInspectionData(models.Model):
    """Table to store the actual results of each daily check."""
    
    STATUS_CHOICES = [
        ('good', 'Good'),
        ('not_good', 'Not Good'),
    ]
    
    inspection_data_id = models.AutoField(primary_key=True)
    report = models.ForeignKey(InspectionReports, on_delete=models.CASCADE, help_text="Links to the inspection report")
    item = models.ForeignKey(ChecklistItems, on_delete=models.CASCADE, help_text="Links to the checklist item")
    inspection_date = models.DateField(help_text="Specific date of the check (e.g., the date for 'Saturday')")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, help_text="Result of the check based on the legend")
    
    class Meta:
        db_table = 'daily_inspection_data'
        verbose_name = 'Daily Inspection Data'
        verbose_name_plural = 'Daily Inspection Data'
        unique_together = ['report', 'item', 'inspection_date']
        ordering = ['inspection_date', 'item__sort_order']
    
    def __str__(self):
        return f"{self.report.report_number} - {self.item.item_description} ({self.inspection_date}): {self.status}"


class ReportNotes(models.Model):
    """Table to store free-text observations."""
    
    note_id = models.AutoField(primary_key=True)
    report = models.ForeignKey(InspectionReports, on_delete=models.CASCADE, help_text="Links to the inspection report")
    note_text = models.TextField(help_text="Content of the note (الملاحظات إن وجدت)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'report_notes'
        verbose_name = 'Report Note'
        verbose_name_plural = 'Report Notes'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Note for {self.report.report_number}: {self.note_text[:50]}..."


class ReportAttachments(models.Model):
    """Table to manage attached files, like photos mentioned on the form."""
    
    attachment_id = models.AutoField(primary_key=True)
    report = models.ForeignKey(InspectionReports, on_delete=models.CASCADE, help_text="Links to the inspection report")
    file_path = models.FileField(upload_to='inspection_attachments/%Y/%m/%d/', help_text="Server path or URL to the stored image/file")
    caption = models.CharField(max_length=200, blank=True, null=True, help_text="Optional description of the attachment")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'report_attachments'
        verbose_name = 'Report Attachment'
        verbose_name_plural = 'Report Attachments'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Attachment for {self.report.report_number}: {self.file_path.name}"
