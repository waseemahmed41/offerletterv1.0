from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('offer_generated', 'Offer Generated'),
        ('offer_sent', 'Offer Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    ROLE_CHOICES = [
        ('frontend', 'Frontend Developer'),
        ('backend', 'Backend Developer'),
        ('machine_learning', 'Machine Learning Engineer'),
        ('full_stack', 'Full Stack Developer'),
        ('ui_ux', 'UI/UX Designer'),
        ('digital_marketing', 'Digital Marketing'),
        ('pr', 'PR Specialist'),
        ('content', 'Content Writer'),
        ('video_editor', 'Video Editor'),
        ('rnd', 'R&D Specialist'),
    ]
    
    work_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    letter_date = models.DateField()
    joining_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by_id = models.IntegerField(null=True, blank=True)  # Store user ID as integer
    created_by_username = models.CharField(max_length=150, null=True, blank=True)  # Store username for reference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'candidates'  # Use Neon PostgreSQL
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.work_id})"
    
    def get_role_display(self):
        """Get human-readable role name"""
        role_dict = dict(self.ROLE_CHOICES)
        return role_dict.get(self.role, self.role)
    
    def save(self, *args, **kwargs):
        if not self.work_id:
            # Generate work_id atomically to avoid conflicts
            from django.db import transaction
            with transaction.atomic():
                # Lock the table to prevent concurrent work_id generation
                self.work_id = self.generate_work_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_work_id():
        last_candidate = Candidate.objects.order_by('-work_id').first()
        if last_candidate and last_candidate.work_id:
            prefix = last_candidate.work_id[:2]
            number = int(last_candidate.work_id[2:]) + 1
            
            # Handle progression from 0A99 to 0B01
            if number > 99:
                # Increment prefix (0A -> 0B, 0B -> 0C, etc.)
                prefix_letter = prefix[1]
                next_letter = chr(ord(prefix_letter) + 1)
                if next_letter <= 'Z':
                    prefix = f"0{next_letter}"
                    number = 1
                else:
                    # If we reach Z, start over with 1A
                    prefix = "1A"
                    number = 1
            
            return f"OA{number:02d}"
        return "OA20"  # Start from OA20

class Template(models.Model):
    ROLE_CHOICES = [
        ('frontend', 'Frontend Developer'),
        ('backend', 'Backend Developer'),
        ('machine_learning', 'Machine Learning Engineer'),
        ('full_stack', 'Full Stack Developer'),
        ('ui_ux', 'UI/UX Designer'),
        ('digital_marketing', 'Digital Marketing'),
        ('pr', 'PR Specialist'),
        ('content', 'Content Writer'),
        ('video_editor', 'Video Editor'),
        ('rnd', 'R&D Specialist'),
    ]
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True, help_text="Leave blank for general template")
    google_doc_id = models.CharField(max_length=100, blank=True, null=True, help_text="Google Doc ID for template")
    file = models.FileField(upload_to='templates/', blank=True, null=True, help_text="Local DOCX file (backup)")
    is_active = models.BooleanField(default=True)
    created_by_id = models.IntegerField(null=True, blank=True)
    created_by_username = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'templates'  # Use existing templates table
    
    def __str__(self):
        if self.role:
            return f"{self.name} ({self.get_role_display()})"
        return self.name

class OfferLetter(models.Model):
    candidate_id = models.IntegerField(null=True, blank=True)  # Store candidate ID as integer
    template_id = models.IntegerField(null=True, blank=True)  # Store template ID as integer
    candidate_work_id = models.CharField(max_length=10, null=True, blank=True)  # Store work ID for reference
    template_name = models.CharField(max_length=100, null=True, blank=True)  # Store template name for reference
    generated_file = models.FileField(upload_to='offer_letters/', null=True, blank=True)  # Keep for migration
    pdf_file = models.FileField(upload_to='offer_letters/pdf/', null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Offer for {self.candidate_work_id or 'Unknown'}"
    
    def get_candidate(self):
        """Get candidate instance"""
        try:
            return Candidate.objects.get(id=self.candidate_id)
        except (Candidate.DoesNotExist, TypeError, ValueError):
            return None
    
    def get_template(self):
        """Get template instance"""
        try:
            return Template.objects.get(id=self.template_id)
        except (Template.DoesNotExist, TypeError, ValueError):
            return None
