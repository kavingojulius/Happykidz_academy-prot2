# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth import get_user_model
from .models import *


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

class FeePaymentInline(admin.TabularInline):
    model = FeePayment
    extra = 1

class DocTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')
    search_fields = ('title',)
    inlines = [StudentInline, FeePaymentInline]  # Include inlines for both student and fee payments

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_number', 'grade', 'doc_title')
    search_fields = ('name',)

class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'reg_number', 'amount',  'date_paid', 'balance')
    search_fields = ('reg_number', 'student_name')

admin.site.register(StudentDet, StudentAdmin)
admin.site.register(FeePayment, FeePaymentAdmin)
admin.site.register(DocTitle, DocTitleAdmin)













