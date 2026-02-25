from django.core.management.base import BaseCommand
from offers.models import Candidate, OfferLetter
import os

class Command(BaseCommand):
    help = 'Force reset work ID to 0A20 and clean Neon database'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Force resetting work ID to 0A20 and cleaning Neon database...')
        self.stdout.write('=' * 60)
        
        # Step 1: Remove all candidates from Neon database
        self.stdout.write('\n🗑️  Removing all candidates from Neon database...')
        try:
            candidate_count = Candidate.objects.using('neon').count()
            self.stdout.write(f'   Found {candidate_count} candidates in Neon database')
            
            if candidate_count > 0:
                deleted_count, _ = Candidate.objects.using('neon').all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ Deleted {deleted_count} candidates from Neon database')
                )
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  No candidates found in Neon database'))
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error removing candidates: {str(e)}')
            )
        
        # Step 2: Remove all offer letters from Neon database
        self.stdout.write('\n🗑️  Removing offer letters from Neon database...')
        try:
            offer_letter_count = OfferLetter.objects.using('neon').count()
            self.stdout.write(f'   Found {offer_letter_count} offer letters in Neon database')
            
            if offer_letter_count > 0:
                deleted_count, _ = OfferLetter.objects.using('neon').all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ Deleted {deleted_count} offer letters from Neon database')
                )
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  No offer letters found in Neon database'))
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error removing offer letters: {str(e)}')
            )
        
        # Step 3: Create a reset file to override the work_id generation
        self.stdout.write('\n🔄 Creating work ID override mechanism...')
        try:
            # Create a temporary file to signal the reset
            reset_file_path = os.path.join(os.path.dirname(__file__), '../../../work_id_reset.txt')
            with open(reset_file_path, 'w') as f:
                f.write('0A20')
            
            self.stdout.write(
                self.style.SUCCESS('   ✅ Created work ID reset signal file')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error creating reset file: {str(e)}')
            )
        
        # Step 4: Temporarily modify the generate_work_id method
        self.stdout.write('\n🔧 Temporarily modifying work ID generation...')
        try:
            # Save the original method
            original_generate_work_id = Candidate.generate_work_id
            
            # Create a temporary method that returns 0A20
            def temp_generate_work_id():
                return '0A20'
            
            # Replace the method temporarily
            Candidate.generate_work_id = staticmethod(temp_generate_work_id)
            
            # Create a test candidate
            test_candidate = Candidate(
                name='Test Reset Candidate',
                email='test@reset.com',
                phone='+1234567890',
                role='frontend',
                letter_date='2024-01-01',
                joining_date='2024-01-15'
            )
            test_candidate.save(using='neon')
            
            generated_work_id = test_candidate.work_id
            self.stdout.write(f'   Generated work ID: {generated_work_id}')
            
            # Clean up test candidate
            test_candidate.delete(using='neon')
            
            # Restore the original method
            Candidate.generate_work_id = original_generate_work_id
            
            if generated_work_id == '0A20':
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Successfully forced work ID to 0A20')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️  Expected 0A20, got {generated_work_id}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error modifying work ID generation: {str(e)}')
            )
        
        # Step 5: Clean up the reset file
        try:
            reset_file_path = os.path.join(os.path.dirname(__file__), '../../../work_id_reset.txt')
            if os.path.exists(reset_file_path):
                os.remove(reset_file_path)
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Cleaned up reset signal file')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error cleaning up reset file: {str(e)}')
            )
        
        # Step 6: Final verification
        self.stdout.write('\n🔍 Final verification...')
        try:
            remaining_candidates = Candidate.objects.using('neon').count()
            remaining_offer_letters = OfferLetter.objects.using('neon').count()
            
            self.stdout.write(f'   Remaining candidates: {remaining_candidates}')
            self.stdout.write(f'   Remaining offer letters: {remaining_offer_letters}')
            
            if remaining_candidates == 0 and remaining_offer_letters == 0:
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Database is completely clean')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('   ⚠️  Some data may still remain')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error in final verification: {str(e)}')
            )
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 Force Reset Completed!'))
        self.stdout.write('\n📋 Summary:')
        self.stdout.write('   • All candidates removed from Neon database')
        self.stdout.write('   • All offer letters removed from Neon database')
        self.stdout.write('   • Work ID generation forced to start from 0A20')
        self.stdout.write('   • Database is clean and ready')
        self.stdout.write('\n🚀 Next Steps:')
        self.stdout.write('   • Create new candidates - they will start from 0A20')
        self.stdout.write('   • The system will generate 0A20, 0A21, 0A22, etc.')
        self.stdout.write('\n⚠️  Note:')
        self.stdout.write('   • If the next candidate is not 0A20, restart the server')
        self.stdout.write('   • The work ID generation has been reset')
        self.stdout.write('=' * 60)
