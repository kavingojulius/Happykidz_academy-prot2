from django.db import models
from django.contrib.auth.models import AbstractUser
import pandas as pd
import openpyxl
from django.contrib.auth import get_user_model  # Use this to get the CustomUser model
from django.conf import settings
# Get the custom user model


# Creating extra field(s) for User in the admin panel
class CustomUser(AbstractUser):
    reg_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    # class Meta:
    #     db_table = 'auth_user'

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
    
# The document to be uploaded containing diff students & their details(excel file)
class DocTitle(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='docs/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.document:  # Check if there is a document uploaded
            self.read_excel_and_create_students()

    def read_excel_and_create_students(self):
        User = get_user_model()  # Get the custom user model instead of the default User
        wb = openpyxl.load_workbook(self.document.path)
        sheet = wb.active
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            name, reg_number, grade = row  # Adjust according to your Excel structure
            # StudentDet.objects.create(doc_title=self, name=name, age=age, grade=grade)

            # Check if there is a parent (user) with the matching reg_number
            try:
                parent = User.objects.get(reg_number=reg_number)
            except User.DoesNotExist:
                parent = None

            if parent:
                # Create or update student record
                # Check if the student already exists
                StudentDet.objects.update_or_create(
                    doc_title=self,
                    name=name,
                    defaults={'reg_number': reg_number, 'grade': grade}
                )

# The student details (has the same fields as the students excel file)
class StudentDet(models.Model):
    doc_title = models.ForeignKey(DocTitle, related_name='students', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=10)

    class Meta:
        unique_together = ('doc_title', 'name')  # Ensures unique name per document

    def __str__(self):
        return self.name

 
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
