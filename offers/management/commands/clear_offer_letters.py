from django.core.management.base import BaseCommand
from offers.models import OfferLetter

class Command(BaseCommand):
    help = 'Remove all rows from offer_letter table in Neon database'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Removing rows from offer_letter table in Neon database...')
        
        # Count existing rows
        existing_count = OfferLetter.objects.using('neon').count()
        self.stdout.write(f'📊 Found {existing_count} rows in offer_letter table')
        
        if existing_count == 0:
            self.stdout.write(self.style.WARNING('⚠️  No rows found in offer_letter table'))
            return
        
        # Remove all rows
        try:
            deleted_count, _ = OfferLetter.objects.using('neon').all().delete()
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully deleted {deleted_count} rows from offer_letter table')
            )
            
            # Verify deletion
            remaining_count = OfferLetter.objects.using('neon').count()
            if remaining_count == 0:
                self.stdout.write(
                    self.style.SUCCESS('✅ Verification: offer_letter table is now empty')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Warning: {remaining_count} rows still remain')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error deleting rows: {str(e)}')
            )
        
        self.stdout.write('\n🎉 Operation completed!')
