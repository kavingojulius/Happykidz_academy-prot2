# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth import get_user_model
from .models import *
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook

User = get_user_model()  # Get the custom user model

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin interface
    fieldsets = UserAdmin.fieldsets + (  # Extending the existing UserAdmin fieldsets
        (None, {'fields': ('reg_number',)}),  # Adding the reg_number field
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('reg_number',)}),  # Add reg_number when creating a user
    )

    # List display to include reg_number
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'reg_number')

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_number', 'class_level', ) #'doc_title'
    search_fields = ('name',)


@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):    
    search_fields = ('name', )    


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('term', 'start_date', 'end_date', 'year')
    list_filter = ('term','year', )
    search_fields = ('term','year',)

@admin.register(TermSection)
class TermSectionAdmin(admin.ModelAdmin):
    list_display = ('term_section',)
    list_filter = ('term_section', )
    search_fields = ('term_section',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    list_filter = ('subject', )
    search_fields = ('subject',)

admin.site.register(Document)

def export_students_to_excel(modeladmin, request, queryset):
    # Create a workbook and a sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Students Data"

    # Define the headers
    headers = ['ADM_NO', 'CHILD_NAME', 'D_O_B', 'CLASS_ENROLLED', 'PREVIOUS_SCHOOL', 'NATIONALITY',
               'FATHERS_NAME', 'FATHERS_CONTACT', 'FATHERS_OCCUPATION', 'FATHERS_LOCATION',
               'MOTHERS_NAME', 'MOTHERS_CONTACT', 'MOTHERS_OCCUPATION', 'RESIDENTIAL', 'RELIGION',
               'GUARDIAN_NAME', 'GUARDIAN_CONTACT', 'HEALTH_STATUS', 'HOSPITAL_RECOMMENDATION', 'ACTIVE_CLUBS']
    ws.append(headers)

    # Add data rows
    for student in queryset:
        row = [student.adm_no, student.child_name, student.d_o_b, student.class_enrolled, student.previous_school,
               student.nationality, student.fathers_name, student.fathers_contact, student.fathers_occupation,
               student.fathers_location, student.mothers_name, student.mothers_contact, student.mothers_occupation,
               student.residential, student.religion, student.guardian_name, student.guardian_contact,
               student.health_status, student.hospital_recommendation, student.active_clubs]
        ws.append(row)

    # Create a response to download the Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students_data.xlsx"'
    wb.save(response)
    return response

class StdAdmin(admin.ModelAdmin):
    list_display = ('adm_no', 'child_name', 'd_o_b', 'class_enrolled', 'previous_school', 'nationality', 'fathers_name', 'fathers_contact', 'fathers_occupation', 'fathers_location', 'mothers_name', 'mothers_contact', 'mothers_occupation', 'residential', 'religion', 'guardian_name', 'guardian_contact', 'health_status', 'hospital_recommendation', 'active_clubs')
    search_fields = ('adm_no', 'child_name', 'd_o_b', 'class_enrolled')
    actions = [export_students_to_excel]

admin.site.register(Students, StdAdmin)

@admin.register(Health)
class HealthAdmin(admin.ModelAdmin):
    list_display = ('student', 'health_status', 'date_recorded')
    list_filter = ('health_status', 'date_recorded','student')
    search_fields = ('student__adm_no',)

def export_fees_to_excel(modeladmin, request, queryset):
    # Create a workbook and a sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "FeesPayment Data"

    # Define the headers
    headers = ['ADM_NO', 'CHILD_NAME', 'CLASS_ENROLLED', 'FEE_PAYMENT', 'AMOUNT_PAID', 
               'MODE_OF_PAYMENT', 'CODE_OR_REF_NO', 'DATE_PAID', 'TIME_PAID', 'BALANCE']
    ws.append(headers)

    # Add data rows
    for fee in queryset:
        row = [fee.adm_no, fee.child_name, fee.class_enrolled, fee.fee_payment, fee.amount_paid,
               fee.mode_of_payment, fee.code_or_ref_no, fee.date_paid, fee.time_paid, fee.balance]
        ws.append(row)

    # Create a response to download the Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="fees_payment.xlsx"'
    wb.save(response)
    return response

@admin.register(FeesPayment)
class FeesPaymentAdmin(admin.ModelAdmin):
    list_display = ('adm_no', 'child_name', 'class_enrolled', 'fee_payment', 'amount_paid', 'mode_of_payment', 'code_or_ref_no', 'date_paid', 'time_paid', 'balance')
    search_fields = ('adm_no', 'child_name', 'class_enrolled')

    actions = [export_fees_to_excel]

@admin.register(ExcelFeeUpload)
class ExcelFeeUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'document')
    search_fields = ('title',)


@admin.register(StudentResults)
class StudentResultsAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'term_section', 'subject', 'marks')
    list_filter = ('student__adm_no','term', 'term_section', 'subject')
    search_fields = ('student__child_name', 'student__adm_no')











