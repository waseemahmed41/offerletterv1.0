from django.core.management.base import BaseCommand
from offers.models import OfferLetter
import os
import stat

class Command(BaseCommand):
    help = 'Clean up PDF files that failed to be removed automatically'

    def handle(self, *args, **options):
        self.stdout.write('🧹 Cleaning up PDF files...')
        
        # Get the PDF directory
        pdf_dir = 'media/offer_letters/pdf'
        
        # Clean up physical files
        if os.path.exists(pdf_dir):
            files_removed = 0
            files_failed = 0
            
            for filename in os.listdir(pdf_dir):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(pdf_dir, filename)
                    try:
                        # Try to remove file
                        os.remove(file_path)
                        files_removed += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Removed: {filename}')
                        )
                    except PermissionError:
                        # Try to change permissions and remove
                        try:
                            os.chmod(file_path, stat.S_IWRITE)
                            os.remove(file_path)
                            files_removed += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'✅ Removed (with permission change): {filename}')
                            )
                        except Exception as e:
                            files_failed += 1
                            self.stdout.write(
                                self.style.ERROR(f'❌ Failed to remove {filename}: {str(e)}')
                            )
                    except Exception as e:
                        files_failed += 1
                        self.stdout.write(
                            self.style.ERROR(f'❌ Failed to remove {filename}: {str(e)}')
                        )
            
            self.stdout.write(f'\n📊 File Cleanup Summary:')
            self.stdout.write(f'   • Files removed: {files_removed}')
            self.stdout.write(f'   • Files failed: {files_failed}')
        
        # Check database for orphaned PDF records
        self.stdout.write('\n🔍 Checking database for orphaned PDF records...')
        orphaned_count = 0
        
        # Check both databases
        databases = ['default', 'neon']
        for db in databases:
            db_name = 'SQLite' if db == 'default' else 'Neon PostgreSQL'
            offer_letters = OfferLetter.objects.using(db).filter(pdf_file__isnull=False)
            
            if offer_letters.exists():
                self.stdout.write(f'\n{db_name} - Found {offer_letters.count()} records with PDF files:')
                for offer_letter in offer_letters:
                    if offer_letter.pdf_file:
                        pdf_path = offer_letter.pdf_file.path
                        if not os.path.exists(pdf_path):
                            # File doesn't exist, clear the database reference
                            offer_letter.pdf_file.delete(save=True)
                            orphaned_count += 1
                            self.stdout.write(
                                self.style.WARNING(f'⚠️  Cleared orphaned reference: {pdf_path}')
                            )
        
        self.stdout.write(f'\n🎉 Cleanup completed!')
        self.stdout.write(f'   • Orphaned references cleared: {orphaned_count}')
        
        # Show final directory status
        if os.path.exists(pdf_dir):
            remaining_files = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
            self.stdout.write(f'   • Remaining PDF files: {remaining_files}')
        else:
            self.stdout.write(f'   • PDF directory does not exist')
