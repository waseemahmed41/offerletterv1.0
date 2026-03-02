from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.conf import settings
from celery.result import AsyncResult
import json
import os

from .models import Candidate, Template, OfferLetter
from .utils import generate_offer_letter, process_bulk_upload, get_template_for_role
from .forms import CandidateForm, TemplateForm
from .email_templates import get_offer_letter_email_content
from .tasks import generate_offer_letter_task

@login_required
def dashboard(request):
    """Main dashboard view"""
    # Get statistics
    total_candidates = Candidate.objects.count()
    pending_candidates = Candidate.objects.filter(status='pending').count()
    offer_generated = Candidate.objects.filter(status='offer_generated').count()
    offer_sent = Candidate.objects.filter(status='offer_sent').count()
    
    # Recent candidates
    recent_candidates = Candidate.objects.order_by('-created_at')[:10]
    
    # Get today's date for letter date display
    from django.utils import timezone
    import pytz
    
    # Use the same timezone as the server
    local_tz = pytz.timezone('Asia/Kolkata')  # UTC+05:30
    today_local = timezone.now().astimezone(local_tz)
    today_date = today_local.strftime('%d %B %Y')
    
    context = {
        'total_candidates': total_candidates,
        'pending_candidates': pending_candidates,
        'offer_generated': offer_generated,
        'offer_sent': offer_sent,
        'recent_candidates': recent_candidates,
        'today_date': today_date,
    }
    
    return render(request, 'offers/dashboard.html', context)

@login_required
def bulk_upload(request):
    """Handle bulk upload of candidates"""
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        file = request.FILES['file']
        
        # Validate file type
        allowed_extensions = ['.csv', '.xlsx', '.xls']
        if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
            return JsonResponse({'error': 'Invalid file type. Please upload CSV or Excel file.'}, status=400)
        
        # Process the file
        try:
            candidates, errors = process_bulk_upload(file, request.user)
        except Exception as e:
            return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=400)
        
        if candidates is None:
            error_msg = errors[0] if errors else 'Unknown error occurred'
            return JsonResponse({'error': error_msg}, status=400)
        
        # Prepare response
        candidate_data = []
        for candidate in candidates:
            candidate_data.append({
                'id': candidate.id,
                'work_id': candidate.work_id,
                'name': candidate.name,
                'email': candidate.email,
                'phone': candidate.phone,
                'role': candidate.role,
                'letter_date': candidate.letter_date.strftime('%Y-%m-%d'),
                'joining_date': candidate.joining_date.strftime('%Y-%m-%d'),
                'status': candidate.status,
            })
        
        return JsonResponse({
            'success': True,
            'candidates': candidate_data,
            'errors': errors,
            'total_uploaded': len(candidates),
        })
    
    return render(request, 'offers/bulk_upload.html')

@login_required
@csrf_exempt
def generate_and_send_offer(request):
    """Generate and send offer letter for a candidate (async with Celery)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            candidate_id = data.get('candidate_id')
            print(f"Received request for candidate_id: {candidate_id}")
            
            # Convert string candidate_id to integer
            try:
                candidate_id = int(candidate_id)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid candidate ID'}, status=400)
            
            # Validate candidate exists
            try:
                candidate = Candidate.objects.get(id=candidate_id)
                print(f"Found candidate: {candidate.name}, role: {candidate.role}")
            except Candidate.DoesNotExist:
                return JsonResponse({'error': 'Candidate not found'}, status=404)
            
            # Queue the task
            task = generate_offer_letter_task.delay(candidate_id)
            print(f"Queued task with ID: {task.id}")
            
            return JsonResponse({
                'status': 'queued',
                'task_id': task.id,
                'message': f'Offer letter generation queued for {candidate.name}'
            }, status=202)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def check_task_status(request, task_id):
    """Check the status of a Celery task"""
    try:
        result = AsyncResult(task_id)
        
        response_data = {
            'task_id': task_id,
            'status': result.status,
            'ready': result.ready(),
        }
        
        if result.ready():
            if result.successful():
                response_data['result'] = result.result
            else:
                response_data['error'] = str(result.info)
        else:
            response_data['progress'] = 'Task is still processing...'
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': f'Failed to check task status: {str(e)}'}, status=500)

@login_required
def candidate_list(request):
    """List all candidates with filtering"""
    candidates = Candidate.objects.order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        candidates = candidates.filter(status=status_filter)
    
    return render(request, 'offers/candidate_list.html', {'candidates': candidates})

class CandidateDetailView(View):
    """Candidate detail view with popup support"""
    
    @method_decorator(login_required)
    def get(self, request, candidate_id):
        candidate = get_object_or_404(Candidate, id=candidate_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON for AJAX/popup requests
            return JsonResponse({
                'id': candidate.id,
                'work_id': candidate.work_id,
                'name': candidate.name,
                'email': candidate.email,
                'phone': candidate.phone,
                'role': candidate.role,
                'letter_date': candidate.letter_date.strftime('%Y-%m-%d'),
                'joining_date': candidate.joining_date.strftime('%Y-%m-%d'),
                'status': candidate.status,
                'created_at': candidate.created_at.strftime('%Y-%m-%d %H:%M'),
            })
        
        return render(request, 'offers/candidate_detail.html', {'candidate': candidate})

@login_required
def create_offer(request):
    """Create individual offer form"""
    # Get today's date for letter date display (same as dashboard)
    from django.utils import timezone
    import pytz
    
    # Use the same timezone as the server
    local_tz = pytz.timezone('Asia/Kolkata')  # UTC+05:30
    today_local = timezone.now().astimezone(local_tz)
    today_date = today_local.strftime('%d %B %Y')
    
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            # Save candidate to Neon database
            candidate = form.save(commit=False)
            
            # Convert role choice to display name if it's a choice value
            if candidate.role in ['frontend', 'backend', 'machine_learning', 'full_stack', 'ui_ux', 'digital_marketing', 'pr', 'content', 'video_editor', 'rnd']:
                role_mapping = dict(Candidate.ROLE_CHOICES)
                candidate.role = role_mapping.get(candidate.role, candidate.role)
            
            candidate.created_by_id = request.user.id
            candidate.created_by_username = request.user.username
            candidate.save()
            
            # Check if user wants to generate and send immediately
            generate_send = request.POST.get('generate_send', False)
            
            if generate_send:
                # Get role-specific template
                template = get_template_for_role(candidate.role)
                if not template:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': 'No template found for this role. Please upload a template first.'})
                    messages.error(request, 'No template found for this role. Please upload a template first.')
                    return redirect('offers:create_offer')
                
                # Generate offer letter
                offer_letter = generate_offer_letter(candidate, template)
                if offer_letter:
                    # Send email with beautiful template
                    try:
                        # Get email content from template
                        email_content = get_offer_letter_email_content(candidate, "T-HOME")
                        
                        print(f"Preparing email to: {candidate.email}")
                        print(f"Email subject: {email_content['subject']}")
                        print(f"Email host: {settings.EMAIL_HOST}")
                        print(f"Email port: {settings.EMAIL_PORT}")
                        print(f"Email user: {settings.EMAIL_HOST_USER}")
                        
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
                        if offer_letter and offer_letter.pdf_file:
                            pdf_path = offer_letter.pdf_file.path
                            print(f"Attaching PDF: {pdf_path}")
                            if os.path.exists(pdf_path):
                                email.attach_file(pdf_path)
                            else:
                                print(f"Warning: PDF file not found at {pdf_path}")
                        
                        print("Sending email...")
                        email.send()
                        print("Email sent successfully")  # Debug line
                        
                        # Clean up PDF after successful email send
                        try:
                            import os
                            import stat
                            if os.path.exists(pdf_path):
                                # Try to remove file with different approaches
                                try:
                                    os.remove(pdf_path)
                                    print(f"Cleaned up PDF: {pdf_path}")
                                except PermissionError:
                                    # Try to change file permissions and remove
                                    os.chmod(pdf_path, stat.S_IWRITE)
                                    os.remove(pdf_path)
                                    print(f"Cleaned up PDF (with permission change): {pdf_path}")
                                except Exception as e:
                                    print(f"Failed to remove PDF: {pdf_path} - Error: {e}")
                                    
                            # Clear the pdf_file field in database
                            offer_letter.pdf_file.delete(save=True)
                        except Exception as cleanup_error:
                            print(f"Warning: Failed to cleanup PDF: {cleanup_error}")
                        
                        # Update status
                        candidate.status = 'offer_sent'
                        candidate.save()
                        offer_letter.sent_at = timezone.now()
                        offer_letter.save()
                        
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({'success': True, 'message': f'Offer letter generated and sent to {candidate.email}!', 'status': 'sent'})
                        messages.success(request, f'Offer letter generated and sent to {candidate.email}!')
                        return redirect('offers:dashboard')
                        
                    except Exception as e:
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({'success': False, 'message': f'Offer letter generated but failed to send email: {str(e)}'})
                        messages.error(request, f'Offer letter generated but failed to send email: {str(e)}')
                        return redirect('offers:dashboard')
                else:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': 'Failed to generate offer letter'})
                    messages.error(request, 'Failed to generate offer letter')
                    return redirect('offers:create_offer')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': f'Candidate {candidate.name} created successfully!', 'status': 'created'})
                messages.success(request, f'Candidate {candidate.name} created successfully!')
                return redirect('offers:dashboard')
    else:
        form = CandidateForm()
    
    return render(request, 'offers/create_offer.html', {'form': form, 'today_date': today_date})


@login_required
def get_next_work_id(request):
    """API endpoint to get the next work ID for preview"""
    try:
        next_work_id = Candidate.generate_work_id()
        return JsonResponse({'work_id': next_work_id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def templates(request):
    """Template management view"""
    templates = Template.objects.all().order_by('-created_at')
    
    context = {
        'templates': templates
    }
    
    return render(request, 'offers/templates.html', context)

@login_required
def upload_template(request):
    """Upload new template with Google Doc ID - Full access only"""
    # Check if user has full access
    full_access_users = ['waseem@thome', 'pratheek@thome']
    if request.user.username not in full_access_users:
        messages.error(request, 'You do not have permission to upload templates.')
        return redirect('offers:templates')
    
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by_id = request.user.id
            template.created_by_username = request.user.username
            template.save()
            
            messages.success(request, f'Template "{template.name}" uploaded successfully!')
            return redirect('offers:templates')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TemplateForm()
    
    return render(request, 'offers/upload_template.html', {'form': form})

@login_required
def edit_template(request, template_id):
    """Edit existing template - Full access only"""
    # Check if user has full access
    full_access_users = ['waseem@thome', 'pratheek@thome']
    if request.user.username not in full_access_users:
        messages.error(request, 'You do not have permission to edit templates.')
        return redirect('offers:templates')
    
    template = get_object_or_404(Template, id=template_id)
    
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, f'Template "{template.name}" updated successfully!')
            return redirect('offers:templates')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TemplateForm(instance=template)
    
    return render(request, 'offers/edit_template.html', {'form': form, 'template': template})

@login_required
def delete_template(request, template_id):
    """Delete template - Full access only"""
    # Check if user has full access
    full_access_users = ['waseem@thome', 'pratheek@thome']
    if request.user.username not in full_access_users:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'You do not have permission to delete templates.'})
        else:
            messages.error(request, 'You do not have permission to delete templates.')
            return redirect('offers:templates')
    
    template = get_object_or_404(Template, id=template_id)
    
    if request.method == 'POST':
        template_name = template.name
        template.delete()
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'Template "{template_name}" deleted successfully'})
        else:
            messages.success(request, f'Template "{template_name}" deleted successfully!')
            return redirect('offers:templates')
    
    # For GET requests, show the delete confirmation page
    return render(request, 'offers/delete_template.html', {'template': template})

@login_required
def cleanup_pdfs(request):
    """Admin-only PDF cleanup view"""
    # Only allow pratheek@thome and waseem@thome users
    allowed_users = ['pratheek@thome', 'waseem@thome']
    if request.user.username not in allowed_users:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Unauthorized access'})
        messages.error(request, 'You are not authorized to perform this action')
        return redirect('offers:dashboard')
    
    if request.method == 'POST':
        try:
            import os
            import stat
            from django.conf import settings
            
            # Get the PDF directory
            pdf_dir = os.path.join(settings.MEDIA_ROOT, 'offer_letters', 'pdf')
            
            files_removed = 0
            files_failed = 0
            orphaned_cleared = 0
            
            # Clean up physical files
            if os.path.exists(pdf_dir):
                for filename in os.listdir(pdf_dir):
                    if filename.endswith('.pdf'):
                        file_path = os.path.join(pdf_dir, filename)
                        try:
                            os.remove(file_path)
                            files_removed += 1
                        except PermissionError:
                            try:
                                os.chmod(file_path, stat.S_IWRITE)
                                os.remove(file_path)
                                files_removed += 1
                            except Exception:
                                files_failed += 1
                        except Exception:
                            files_failed += 1
            
            # Check database for orphaned PDF records
            offer_letters = OfferLetter.objects.filter(pdf_file__isnull=False)
            
            for offer_letter in offer_letters:
                if offer_letter.pdf_file:
                    pdf_path = offer_letter.pdf_file.path
                    if not os.path.exists(pdf_path):
                        # File doesn't exist, clear the database reference
                        offer_letter.pdf_file.delete(save=True)
                        orphaned_cleared += 1
            
            # Calculate remaining files
            remaining_files = 0
            if os.path.exists(pdf_dir):
                remaining_files = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
            
            # Debug information
            print(f"DEBUG: Cleanup completed - Files removed: {files_removed}, Failed: {files_failed}, Orphaned: {orphaned_cleared}, Remaining: {remaining_files}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'files_removed': files_removed,
                    'files_failed': files_failed,
                    'orphaned_cleared': orphaned_cleared,
                    'remaining_files': remaining_files
                })
            
            messages.success(request, f'PDF cleanup completed! Removed {files_removed} files, cleared {orphaned_cleared} orphaned references.')
            return redirect('offers:dashboard')
            
        except Exception as e:
            print(f"DEBUG: Cleanup error: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, f'Error during cleanup: {str(e)}')
            return redirect('offers:dashboard')
    
    # For GET requests, redirect to dashboard
    return redirect('offers:dashboard')
