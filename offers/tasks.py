import os
import stat
import logging
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import Candidate, OfferLetter
from .utils import generate_offer_letter, get_template_for_role
from .email_templates import get_offer_letter_email_content

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_offer_letter_task(self, candidate_id):
    """
    Generate and send offer letter for a candidate asynchronously.
    
    Args:
        candidate_id (int): ID of the candidate to generate offer letter for
        
    Returns:
        dict: Result with status, candidate_id, candidate_name on success
    """
    try:
        logger.info(f"Starting offer letter generation task for candidate_id: {candidate_id}")
        
        # Get candidate
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            logger.info(f"Found candidate: {candidate.name}, role: {candidate.role}")
        except Candidate.DoesNotExist:
            logger.error(f"Candidate with ID {candidate_id} does not exist")
            # Don't retry for Candidate.DoesNotExist
            return {
                'status': 'error',
                'error': f'Candidate with ID {candidate_id} does not exist',
                'candidate_id': candidate_id
            }
        
        # Get role-specific template
        template = get_template_for_role(candidate.role)
        if not template:
            error_msg = f'No template found for role: {candidate.role}'
            logger.error(error_msg)
            # Don't retry for template not found
            return {
                'status': 'error',
                'error': error_msg,
                'candidate_id': candidate_id,
                'candidate_name': candidate.name
            }
        
        logger.info(f"Found template: {template.name}, google_doc_id: {template.google_doc_id}")
        
        # Generate offer letter
        logger.info("Starting offer letter generation...")
        offer_letter = generate_offer_letter(candidate, template)
        if not offer_letter:
            error_msg = 'Failed to generate offer letter'
            logger.error(error_msg)
            raise Exception(error_msg)
        
        logger.info("Offer letter generated successfully")
        
        # Send email with beautiful template
        logger.info("Starting email sending...")
        try:
            # Get email content from template
            email_content = get_offer_letter_email_content(candidate, "Your Company")
            
            email = EmailMessage(
                email_content['subject'],
                email_content['text_content'],  # Fallback text content
                settings.DEFAULT_FROM_EMAIL,
                [candidate.email]
            )
            
            # Add HTML content
            email.content_subtype = 'html'
            email.body = email_content['html_content']
            
            # Attach the offer letter (PDF only)
            pdf_path = offer_letter.pdf_file.path
            email.attach_file(pdf_path)
            email.send()
            
            logger.info(f"Email sent successfully to {candidate.email}")
            
            # Clean up PDF after successful email send
            try:
                if os.path.exists(pdf_path):
                    # Try to remove file with different approaches
                    try:
                        os.remove(pdf_path)
                        logger.info(f"Cleaned up PDF: {pdf_path}")
                    except PermissionError:
                        # Try to change file permissions and remove
                        os.chmod(pdf_path, stat.S_IWRITE)
                        os.remove(pdf_path)
                        logger.info(f"Cleaned up PDF (with permission change): {pdf_path}")
                    except Exception as e:
                        logger.warning(f"Failed to remove PDF: {pdf_path} - Error: {e}")
                        
                # Clear the pdf_file field in database
                offer_letter.pdf_file.delete(save=True)
            except Exception as cleanup_error:
                logger.warning(f"Warning: Failed to cleanup PDF: {cleanup_error}")
            
            # Update status
            candidate.status = 'offer_sent'
            candidate.save()
            offer_letter.sent_at = timezone.now()
            offer_letter.save()
            
            logger.info(f"Task completed successfully for candidate: {candidate.name}")
            
            return {
                'status': 'success',
                'candidate_id': candidate_id,
                'candidate_name': candidate.name,
                'message': f'Offer letter generated and sent to {candidate.email}'
            }
            
        except Exception as e:
            error_msg = f'Failed to send email: {str(e)}'
            logger.error(error_msg)
            raise Exception(error_msg)
            
    except Exception as e:
        logger.error(f"Error in generate_offer_letter_task: {str(e)}")
        
        # Retry logic for general exceptions
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying task (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(exc=e, countdown=self.default_retry_delay)
        else:
            logger.error(f"Max retries reached for candidate_id: {candidate_id}")
            return {
                'status': 'error',
                'error': f'Failed after {self.max_retries} retries: {str(e)}',
                'candidate_id': candidate_id,
                'candidate_name': candidate.name if 'candidate' in locals() else 'Unknown'
            }
