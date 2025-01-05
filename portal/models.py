from django.db import models
from django.contrib.auth.models import AbstractUser
import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
import openpyxl
from django.contrib.auth import get_user_model  # Use this to get the CustomUser model
from django.conf import settings
from django.core.exceptions import ValidationError

# ------- custom user model ---- Creating extra field(s) for User in the admin panel  ------

class CustomUser(AbstractUser):
    reg_number = models.CharField(max_length=20, unique=True, blank=True, null=True)    

# Add related_name to avoid conflicts with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Custom related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f"{self.username} ({self.reg_number})"
        

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field to track if a message is read

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.message[:50]}'

    class Meta:
        ordering = ['timestamp']  # Messages will be ordered by time


class ClassLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Grade 1", "Grade 2"    

    class Meta:
        verbose_name_plural = 'Class , Grade etc'

    def __str__(self):
        return f"{self.name}"


class Subject(models.Model):
    subject = models.CharField(max_length=50)    

    class Meta:
        pass

    def __str__(self):
        return f"{self.subject}"


class Term(models.Model):
    term = models.CharField(max_length=50 )    
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    year = models.DateField(blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return f"{self.term}"
    
class TermSection(models.Model):
    term_section = models.CharField(max_length=50)        

    class Meta:
        pass

    def __str__(self):
        return f"{self.term_section}"


class Document(models.Model):

    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='excel_docs/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.document: # Check if there is a document uploaded
            self.read_excel_and_create_students()
    class Meta:
        verbose_name_plural = 'Student details excel upload'
    
    def __str__(self):
        return self.title

    def read_excel_and_create_students(self):
        wb = openpyxl.load_workbook(self.document.path)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
        
            ADM_NO, CHILD_NAME, D_O_B, CLASS_ENROLLED, PREVIOUS_SCHOOL, NATIONALITY, FATHERS_NAME, FATHERS_CONTACT, FATHERS_OCCUPATION, FATHERS_LOCATION, MOTHERS_NAME, MOTHERS_CONTACT, MOTHERS_OCCUPATION, RESIDENTIAL, RELIGION, GUARDIANS_NAME, GUARDIANS_CONTACT, HEALTH, HOSPITAL_RECCOMMENDATION, ACTIVE_CLUBS = row
            
            Students.objects.update_or_create(
                # doc_title=self,
                adm_no=ADM_NO,
                defaults={'child_name': CHILD_NAME,
                        'd_o_b': D_O_B, 
                        'class_enrolled': CLASS_ENROLLED,
                        'previous_school': PREVIOUS_SCHOOL,
                        'nationality': NATIONALITY,
                        'fathers_name': FATHERS_NAME,
                        'fathers_contact': FATHERS_CONTACT,
                        'fathers_occupation': FATHERS_OCCUPATION,
                        'fathers_location': FATHERS_LOCATION,
                        'mothers_name': MOTHERS_NAME,
                        'mothers_contact': MOTHERS_CONTACT,
                        'mothers_occupation': MOTHERS_OCCUPATION,
                        'residential': RESIDENTIAL,
                        'religion': RELIGION,
                        'guardian_name': GUARDIANS_NAME,
                        'guardian_contact': GUARDIANS_CONTACT,
                        'health_status': HEALTH,
                        'hospital_recommendation': HOSPITAL_RECCOMMENDATION,
                        'active_clubs': ACTIVE_CLUBS,
                    }
            )
        

class Students(models.Model):        
    adm_no = models.CharField(max_length=100, unique=True)
    child_name = models.CharField(max_length=100, null=True, blank=True)
    d_o_b = models.CharField(max_length=10, null=True, blank=True)
    class_enrolled = models.CharField(max_length=10, null=True, blank=True)

    previous_school = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    fathers_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_contact = models.CharField(max_length=100, null=True, blank=True)
    fathers_occupation = models.CharField(max_length=100, null=True, blank=True)
    fathers_location = models.CharField(max_length=100, null=True, blank=True)
    mothers_name = models.CharField(max_length=100, null=True, blank=True)
    mothers_contact = models.CharField(max_length=100, null=True, blank=True)
    mothers_occupation = models.CharField(max_length=100, null=True, blank=True)
    residential = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_contact = models.CharField(max_length=100, null=True, blank=True)
    health_status = models.CharField(max_length=100, null=True, blank=True)
    hospital_recommendation = models.CharField(max_length=100, null=True, blank=True)
    active_clubs = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Student Details' 


    def __str__(self):
        
        return f"Student {self.adm_no}"
        
    
class Health(models.Model):
    # Link to a specific student
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="health_information")
    
    # Health status
    health_status = models.CharField(
        max_length=50, 
        choices=[
            ('Excellent', 'Excellent'),
            ('Good', 'Good'),
            ('Average', 'Average'),
            ('Poor', 'Poor')
        ],
        default='Good',
        help_text="Overall health status"
    )
    
    # Additional notes
    notes = models.TextField(blank=True, help_text="Additional health notes")
    
    # Date of the record
    date_recorded = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_recorded']        
        verbose_name_plural = "Health Information"

    def __str__(self):
        return f"{self.student.child_name}'s Health Record on {self.date_recorded}"


class ExcelFeeUpload(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='excel_docs/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.document: # Check if there is a document uploaded
            self.read_excel_and_create_payments()

    class Meta:
        verbose_name_plural = 'Fee excel Upload'

    def __str__(self):
        return self.title   
    
    def read_excel_and_create_payments(self):
        wb = openpyxl.load_workbook(self.document.path)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            
            ADM_NO, CHILD_NAME, CLASS_ENROLLED, FEE_PAYMENT, AMOUNT_PAID, MODE_OF_PAYMENT, CODE_OR_REF_NO, DATE_PAID, TIME_PAID, BALANCE = row

            FeesPayment.objects.update_or_create(
                adm_no=ADM_NO,
                defaults={'child_name': CHILD_NAME,
                        'class_enrolled': CLASS_ENROLLED,
                        'fee_payment': FEE_PAYMENT,
                        'amount_paid': AMOUNT_PAID,
                        'mode_of_payment': MODE_OF_PAYMENT,
                        'code_or_ref_no': CODE_OR_REF_NO,
                        'date_paid': DATE_PAID,
                        'time_paid': TIME_PAID,
                        'balance': BALANCE,
                    }
            )


class FeesPayment(models.Model):

    adm_no = models.CharField(max_length=100, unique=True)
    child_name = models.CharField(max_length=100, null=True, blank=True)
    class_enrolled = models.CharField(max_length=100, null=True, blank=True)
    fee_payment = models.CharField(max_length=100, null=True, blank=True)
    amount_paid = models.CharField(max_length=100, null=True, blank=True)
    mode_of_payment = models.CharField(max_length=100, null=True, blank=True)
    code_or_ref_no = models.CharField(max_length=100, null=True, blank=True)
    date_paid = models.CharField(max_length=100, null=True, blank=True)
    time_paid = models.CharField(max_length=100, null=True, blank=True)
    balance = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Fee Records'

    def __str__(self):
        return f"Fee Upload {self.adm_no}"

class StudentResults(models.Model):
    
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_records")
    term = models.ForeignKey('Term', on_delete=models.CASCADE, related_name="student_records")
    term_section = models.ForeignKey('TermSection', on_delete=models.CASCADE, related_name="student_records")
    date_recorded = models.DateField(blank=True, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="student_records")
    marks =  models.PositiveIntegerField()

    class Meta:
        pass

    def __str__(self):
        return f"{self.student.adm_no} - {self.term} ({self.date_recorded})"
    
    def clean(self):
        # Validate against duplicate subject, term, term section, and year (ignore marks)
        existing_results =  StudentResults.objects.filter(
            student=self.student,
            term=self.term,
            term_section=self.term_section,
            subject=self.subject,
            term__year=self.term.year,  # Check the year
        )
        if self.pk:
            existing_results = existing_results.exclude(pk=self.pk)  # Exclude current instance if editing
        if existing_results.exists():
            raise ValidationError(
                f"A result for {self.student.child_name} in {self.subject} "
                f"({self.term} - {self.term_section}, Year: {self.term.year}) already exists."
            )

    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super().save(*args, **kwargs)



