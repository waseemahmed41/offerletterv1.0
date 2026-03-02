from django import forms
from django.core.validators import RegexValidator
from django.utils import timezone
import pytz
from .models import Candidate, Template

# Role choices for dropdown
ROLE_CHOICES = [
    ('', 'Select Role...'),
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

class CandidateForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890'
        })
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'role-select'
        })
    )
    
    joining_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set letter date to today's date in Asia/Kolkata timezone and make it hidden
        local_tz = pytz.timezone('Asia/Kolkata')
        today_local = timezone.now().astimezone(local_tz)
        self.fields['letter_date'] = forms.DateField(
            initial=today_local.date(),
            widget=forms.HiddenInput()
        )
    
    class Meta:
        model = Candidate
        fields = ['name', 'email', 'phone', 'role', 'letter_date', 'joining_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
        }

class TemplateForm(forms.ModelForm):
    """Form for creating/updating templates with Google Doc ID"""
    
    google_doc_id = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Google Doc ID (e.g., 1iALpheZ7E4dE5ULqERe8Db0q7ZK32m0xEE9PrHPZz2o)',
            'help_text': 'Get this from Google Docs URL: docs.google.com/document/d/DOC_ID/edit'
        })
    )
    
    class Meta:
        model = Template
        fields = ['name', 'role', 'file', 'google_doc_id']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter template name'
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter role name (e.g., Frontend Developer, Backend Developer, UI/UX Designer)',
                'help_text': 'Enter the role name as it should appear in the offer letter dropdown'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.docx,.doc'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing template, populate google_doc_id
        if self.instance and self.instance.pk:
            self.fields['google_doc_id'].initial = self.instance.google_doc_id
