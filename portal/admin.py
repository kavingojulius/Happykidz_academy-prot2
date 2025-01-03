# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth import get_user_model
from .models import *
import pandas as pd


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


class StudentInline(admin.TabularInline):
    model = StudentDet
    extra = 1  # Allows adding one more student by default


class DocTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')
    search_fields = ('title',)    

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_number', 'class_level', ) #'doc_title'
    search_fields = ('name',)

admin.site.register(StudentDet, StudentAdmin)
admin.site.register(DocTitle, DocTitleAdmin)

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'reg_number', 'amount', 'date_paid', 'balance', 'document')
    fieldsets = (
        (None, {
            'fields': ('student_name', 'reg_number', 'amount', 'date_paid', 'balance', 'document')
        }),
    )
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # Check if the object is new
        super().save_model(request, obj, form, change)
        
        # After saving the model, process the file if it's new and has a document
        if is_new and obj.document:
            obj.process_excel_file()


@admin.register(HealthProgress)
class HealthProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'health_status', 'date_recorded')
    list_filter = ('health_status', 'date_recorded')
    search_fields = ('student__reg_number',)

@admin.register(FeePay)
class FeePayAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'total_amount_paid', 'date_paid')
    list_filter = ('term', 'date_paid')
    fields = ('student', 'term', 'amounts', 'date_paid')
    search_fields = ('student','term')

    def total_amount_paid(self, obj):
        return obj.total_amount_paid()


@admin.register(TermFee)
class TermFeeAdmin(admin.ModelAdmin):
    list_display = ('class_level', 'term', 'fee', 'year')
    list_filter = ('class_level', 'term', 'year')
    search_fields = ('class_level', 'term', 'year')

@admin.register(PayFee)
class PayFeeAdmin(admin.ModelAdmin):
    # Define what fields you want to display in the list view
    list_display = ('student', 'term', 'date_paid', 'transaction_mode', 'amount')
    
    # Add filters to easily filter records by 'term' and 'date_paid'
    list_filter = ('student__reg_number','term', 'date_paid')
    
    # Define which fields should be searchable in the admin
    search_fields = ('student__reg_number', 'term', 'date_paid')
    
    # Optional: Allow editing the amount and transaction mode directly in the admin
    fieldsets = (
        (None, {
            'fields': ('student', 'term', 'date_paid', 'transaction_mode', 'amount',)
        }),
    )
        
    
    # Customize how the model is saved, if necessary
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):    
    search_fields = ('name', )    

@admin.register(Results)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'term_section', 'subject', 'marks')
    list_filter = ('student__reg_number','term', 'term_section', 'subject')
    search_fields = ('student__name', 'student__reg_number')

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






