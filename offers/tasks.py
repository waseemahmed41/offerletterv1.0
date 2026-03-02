from celery import shared_task
from .models import Candidate, OfferLetter
from .utils import generate_offer_letter
from django.core.mail import EmailMessage
from django.conf import settings
import os

@shared_task(bind=True, max_retries=3)
def generate_and_send_offer_async(self, candidate_id):
    """
    Asynchronous offer letter generation and email sending
    Prevents worker timeouts by running in background
    """
    try:
        # Get candidate
        candidate = Candidate.objects.get(id=candidate_id)
        
        # Get template
        from .utils import get_template_for_role
        template = get_template_for_role(candidate.role)
        
        if not template:
            return {'status': 'error', 'message': 'No template found'}
        
        # Generate offer letter (this runs in background)
        offer_letter = generate_offer_letter(candidate, template)
        
        if offer_letter:
            # Send email
            try:
                from .utils import get_offer_letter_email_content
                email_content = get_offer_letter_email_content(candidate, "T-HOME")
                
                email = EmailMessage(
                    email_content['subject'],
                    email_content['text_content'],
                    settings.DEFAULT_FROM_EMAIL,
                    [candidate.email]
                )
                
                email.content_subtype = 'html'
                email.body = email_content['html_content']
                
                # Attach PDF
                if offer_letter.pdf_file and os.path.exists(offer_letter.pdf_file.path):
                    email.attach_file(offer_letter.pdf_file.path)
                
                email.send()
                
                return {'status': 'success', 'offer_letter_id': offer_letter.id}
                
            except Exception as e:
                return {'status': 'error', 'message': f'Email failed: {str(e)}'}
        
        return {'status': 'error', 'message': 'Failed to generate offer letter'}
        
    except Exception as e:
        return {'status': 'error', 'message': f'Task failed: {str(e)}'}
