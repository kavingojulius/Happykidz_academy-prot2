from django.contrib import admin
from .models import *
from openpyxl import Workbook
from django.http import HttpResponse

# Register your models here.
@admin.register(DownloadMaterials)
class DownloadMaterialsAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

admin.site.register(Gallery)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_event_active')

admin.site.register(Event, EventAdmin)

admin.site.register(LandingPageText)
admin.site.register(News)


def export_admissions_to_excel(modeladmin, request, queryset):
    # Create a Workbook object
    wb = Workbook()
    ws = wb.active
    ws.title = "Admission Requests"

# Define the headers in the specified format
    headers = [
        "CHILD_NAME", "D_O_B", "CLASS_ENROLLED", "PREVIOUS_SCHOOL",
        "FATHERS_NAME", "FATHERS_CONTACT", "FATHERS_OCCUPATION", "FATHERS_LOCATION",
        "MOTHERS_NAME", "MOTHERS_CONTACT", "MOTHERS_OCCUPATION", "RESIDENTIAL", "RELIGION",
        "GUARDIANS_NAME", "GUARDIANS_CONTACT", "HEALTH", "HOSPITAL_RECCOMMENDATION", "ACTIVE_CLUBS"
    ]
    
    # Add headers to the worksheet
    ws.append(headers)

    # Add data rows from the queryset
    for admission in queryset:
        row = [
            admission.child_name, admission.d_o_b, admission.class_enrolled, admission.previous_school,
            admission.fathers_name, admission.fathers_contact, admission.fathers_occupation, admission.fathers_location,
            admission.mothers_name, admission.mothers_contact, admission.mothers_occupation, admission.residential,
            admission.religion, admission.guardian_name, admission.guardian_contact, admission.health_status,
            admission.hospital_recommendation, admission.active_clubs
        ]
        ws.append(row)

    # Create the HTTP response with the Excel file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="admission_requests.xlsx"'

    # Save the workbook to the response object
    wb.save(response)
    return response

export_admissions_to_excel.short_description = "Export Selected Admissions to Excel"

# Register the model with the custom action
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['child_name', 'class_enrolled', 'submitted_at']
    actions = [export_admissions_to_excel]

admin.site.register(Admission, AdmissionAdmin)


