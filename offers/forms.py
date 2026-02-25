from django import forms
from django.core.validators import RegexValidator
from django.utils import timezone
import pytz
from .models import Candidate

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
        choices=[('', 'Select Role')] + list(Candidate.ROLE_CHOICES),
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
