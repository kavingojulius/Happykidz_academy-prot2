from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class LandingPageText(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    

class Event(models.Model):
    title = models.CharField(max_length=255)  # Title of the event
    image = models.ImageField(upload_to='events_images')  # Image field for the event
    content = models.TextField()  # Content description of the event
    start_time = models.DateTimeField()  # Event start time
    end_time = models.DateTimeField()  # Event end time
    
    def is_event_active(self):
        """Check if the event is still active (current time is before end time)"""
        return timezone.now() < self.end_time
    
    def time_remaining(self):
        """Calculate time remaining until the event ends"""
        if self.is_event_active():
            return self.end_time - timezone.now()
        return None
    
    def __str__(self):
        return self.title


class DownloadMaterials(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='Download_Materials/') # Files will be uploaded to MEDIA_ROOT/pdfs
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Download Materials(such as PDFS,... etc)'
    

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Gallery (images)'

    
class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'News'


class Admission(models.Model):
    # Student Information
    child_name = models.CharField(max_length=100)
    d_o_b = models.CharField(max_length=10)  # Date of Birth as string (in 'YYYY-MM-DD' format)
    class_enrolled = models.CharField(max_length=10)
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    
    # Parent/Guardian Information
    fathers_name = models.CharField(max_length=100)
    fathers_contact = models.CharField(max_length=100)
    fathers_occupation = models.CharField(max_length=100)
    fathers_location = models.CharField(max_length=100)
    
    mothers_name = models.CharField(max_length=100)
    mothers_contact = models.CharField(max_length=100)
    mothers_occupation = models.CharField(max_length=100)
    residential = models.CharField(max_length=100)
    
    # Guardian and Health Information
    religion = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=100)
    health_status = models.CharField(max_length=100)
    hospital_recommendation = models.CharField(max_length=100)
    active_clubs = models.CharField(max_length=100)

    # Timestamp
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child_name} - {self.class_enrolled}"

    class Meta:
        verbose_name_plural = 'Admission Requests'





