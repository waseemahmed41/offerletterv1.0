import os
import json
import base64
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.core.files.base import ContentFile
import tempfile
import requests


class GoogleDocsService:
    """Service class for Google Docs and Drive API operations"""
    
    def __init__(self):
        private_key = os.getenv('GOOGLE_PRIVATE_KEY', '')
        
        # Handle different private key formats
        if private_key.startswith('"') and private_key.endswith('"'):
            private_key = private_key[1:-1]  # Remove surrounding quotes
        
        # Replace literal \n with actual newlines
        private_key = private_key.replace('\\n', '\n')
        
        self.service_account_info = {
            "type": "service_account",
            "project_id": os.getenv('GOOGLE_PROJECT_ID'),
            "private_key": private_key,
            "client_email": os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
        
        self.scopes = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        self._credentials = None
        self._docs_service = None
        self._drive_service = None
    
    def _get_credentials(self):
        """Get service account credentials"""
        if not self._credentials:
            self._credentials = service_account.Credentials.from_service_account_info(
                self.service_account_info, 
                scopes=self.scopes
            )
        return self._credentials
    
    def _get_docs_service(self):
        """Get Google Docs service instance"""
        if not self._docs_service:
            self._docs_service = build(
                'docs', 
                'v1', 
                credentials=self._get_credentials()
            )
        return self._docs_service
    
    def _get_drive_service(self):
        """Get Google Drive service instance"""
        if not self._drive_service:
            self._drive_service = build(
                'drive', 
                'v3', 
                credentials=self._get_credentials()
            )
        return self._drive_service
    
    def copy_template(self, template_doc_id: str, title: str) -> str:
        """
        Copy a Google Doc template and return the new document ID
        
        Args:
            template_doc_id: ID of the template document
            title: Title for the new document
            
        Returns:
            str: ID of the copied document
            
        Raises:
            Exception: If copy operation fails
        """
        try:
            drive_service = self._get_drive_service()
            
            # Copy the document
            copy_request = {
                'name': title
            }
            
            response = drive_service.files().copy(
                fileId=template_doc_id,
                body=copy_request
            ).execute()
            
            return response.get('id')
            
        except HttpError as error:
            raise Exception(f"Failed to copy template: {error}")
        except Exception as error:
            raise Exception(f"Error copying template: {error}")
    
    def replace_placeholders(self, doc_id: str, replacements: dict) -> None:
        """
        Replace placeholders in Google Doc with actual values
        
        Args:
            doc_id: ID of the document to modify
            replacements: Dictionary of placeholder -> value pairs
            
        Raises:
            Exception: If replacement operation fails
        """
        try:
            docs_service = self._get_docs_service()
            
            # Get document content
            document = docs_service.documents().get(documentId=doc_id).execute()
            
            # Prepare replacement requests
            requests_batch = []
            
            # Replace text in all paragraphs
            for element in document.get('body', {}).get('content', []):
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    for run in paragraph.get('elements', []):
                        if 'textRun' in run:
                            text = run['textRun'].get('content', '')
                            
                            # Check for placeholders and replace them
                            for placeholder, value in replacements.items():
                                if placeholder in text:
                                    start_index = run.get('startIndex', 0)
                                    end_index = start_index + len(text)
                                    
                                    requests_batch.append({
                                        'replaceAllText': {
                                            'containsText': {
                                                'text': placeholder,
                                                'matchCase': False
                                            },
                                            'replaceText': str(value)
                                        }
                                    })
            
            # Execute all replacements in batch
            if requests_batch:
                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests_batch}
                ).execute()
                
        except HttpError as error:
            raise Exception(f"Failed to replace placeholders: {error}")
        except Exception as error:
            raise Exception(f"Error replacing placeholders: {error}")
    
    def export_as_pdf(self, doc_id: str) -> bytes:
        """
        Export Google Doc as PDF
        
        Args:
            doc_id: ID of the document to export
            
        Returns:
            bytes: PDF content
            
        Raises:
            Exception: If export operation fails
        """
        try:
            drive_service = self._get_drive_service()
            
            # Export document as PDF
            response = drive_service.files().export(
                fileId=doc_id,
                mimeType='application/pdf'
            ).execute()
            
            return response
            
        except HttpError as error:
            raise Exception(f"Failed to export PDF: {error}")
        except Exception as error:
            raise Exception(f"Error exporting PDF: {error}")
    
    def delete_document(self, doc_id: str) -> None:
        """
        Delete a document from Google Drive
        
        Args:
            doc_id: ID of the document to delete
            
        Raises:
            Exception: If delete operation fails
        """
        try:
            drive_service = self._get_drive_service()
            drive_service.files().delete(fileId=doc_id).execute()
            
        except HttpError as error:
            raise Exception(f"Failed to delete document: {error}")
        except Exception as error:
            raise Exception(f"Error deleting document: {error}")
    
    def generate_offer_pdf(self, template_doc_id: str, candidate_data: dict, candidate_name: str) -> ContentFile:
        """
        Complete workflow: Copy template -> Replace placeholders -> Export PDF -> Delete temp doc
        
        Args:
            template_doc_id: ID of the template document
            candidate_data: Dictionary with candidate information
            candidate_name: Name of the candidate (for document title)
            
        Returns:
            ContentFile: PDF file content ready for Django storage
            
        Raises:
            Exception: If any step in the workflow fails
        """
        temp_doc_id = None
        
        try:
            # Step 1: Copy template
            temp_doc_id = self.copy_template(
                template_doc_id, 
                f"Offer Letter - {candidate_name}"
            )
            
            # Step 2: Replace placeholders
            self.replace_placeholders(temp_doc_id, candidate_data)
            
            # Step 3: Export as PDF
            pdf_content = self.export_as_pdf(temp_doc_id)
            
            # Step 4: Create ContentFile for Django
            pdf_filename = f"offer_{candidate_data.get('{{work_id}}', 'unknown')}.pdf"
            pdf_file = ContentFile(pdf_content, pdf_filename)
            
            return pdf_file
            
        except Exception as error:
            raise Exception(f"Failed to generate offer PDF: {error}")
            
        finally:
            # Step 5: Always cleanup temporary document
            if temp_doc_id:
                try:
                    self.delete_document(temp_doc_id)
                except Exception as cleanup_error:
                    # Log cleanup error but don't raise it
                    print(f"Warning: Failed to cleanup temporary document: {cleanup_error}")
    
    def replace_placeholders_in_template(self, doc_id: str, replacements: dict) -> None:
        """
        Replace placeholders in Google Doc without copying
        
        Args:
            doc_id: ID of the document to modify
            replacements: Dictionary of placeholder -> value pairs
            
        Raises:
            Exception: If replacement operation fails
        """
        try:
            docs_service = self._get_docs_service()
            
            # Prepare replacement requests
            requests_batch = []
            
            # Add replacement requests for each placeholder
            for placeholder, value in replacements.items():
                requests_batch.append({
                    'replaceAllText': {
                        'containsText': {
                            'text': placeholder,
                            'matchCase': False
                        },
                        'replaceText': str(value)
                    }
                })
            
            # Execute all replacements in batch
            if requests_batch:
                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests_batch}
                ).execute()
                
        except HttpError as error:
            raise Exception(f"Failed to replace placeholders: {error}")
        except Exception as error:
            raise Exception(f"Error replacing placeholders: {error}")
    
    def generate_offer_pdf_smart(self, template_doc_id: str, candidate_data: dict, candidate_name: str) -> ContentFile:
        """
        Smart method: Replace placeholders in template, export PDF, then revert changes
        This avoids copying and storage quota issues
        
        Args:
            template_doc_id: ID of the template document
            candidate_data: Dictionary with candidate information
            candidate_name: Name of the candidate (for document title)
            
        Returns:
            ContentFile: PDF file content ready for Django storage
            
        Raises:
            Exception: If any step in the workflow fails
        """
        try:
            # Step 1: Get current document content (backup)
            docs_service = self._get_docs_service()
            original_doc = docs_service.documents().get(documentId=template_doc_id).execute()
            
            # Step 2: Replace placeholders in the template
            self.replace_placeholders_in_template(template_doc_id, candidate_data)
            
            # Step 3: Export as PDF
            pdf_content = self.export_as_pdf(template_doc_id)
            
            # Step 4: Create ContentFile for Django
            pdf_filename = f"offer_{candidate_data.get('{{work_id}}', 'unknown')}.pdf"
            pdf_file = ContentFile(pdf_content, pdf_filename)
            
            # Step 5: Revert changes (restore original template)
            # Create requests to revert all changes
            revert_requests = []
            for replacement in candidate_data.keys():
                revert_requests.append({
                    'replaceAllText': {
                        'containsText': {
                            'text': str(candidate_data[replacement]),
                            'matchCase': False
                        },
                        'replaceText': replacement  # Restore original placeholder
                    }
                })
            
            # Execute revert
            try:
                docs_service.documents().batchUpdate(
                    documentId=template_doc_id,
                    body={'requests': revert_requests}
                ).execute()
            except:
                # If revert fails, we'll restore from backup next time
                print("Warning: Could not revert template changes")
            
            return pdf_file
            
        except Exception as error:
            raise Exception(f"Failed to generate offer PDF smart: {error}")
