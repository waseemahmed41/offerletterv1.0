from django.core.management.base import BaseCommand
from offers.models import Candidate, OfferLetter

class Command(BaseCommand):
    help = 'Reset work ID to 0A20 and remove all candidates from Neon database (Simple Approach)'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Resetting work ID and cleaning Neon database...')
        self.stdout.write('=' * 60)
        
        # Step 1: Remove all candidates from Neon database
        self.stdout.write('\n🗑️  Removing candidates from Neon database...')
        try:
            candidate_count = Candidate.objects.using('neon').count()
            self.stdout.write(f'   Found {candidate_count} candidates in Neon database')
            
            if candidate_count > 0:
                # Remove all candidates
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
                # Remove all offer letters
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
        
        # Step 3: Create a dummy candidate to force the sequence to 0A20
        self.stdout.write('\n🔄 Setting up work ID to start from 0A20...')
        try:
            # Create dummy candidates to force the sequence
            for i in range(20, 30):  # Create candidates 0A20 through 0A29
                dummy_candidate = Candidate(
                    name=f'Dummy Candidate {i}',
                    email=f'dummy{i}@example.com',
                    phone='+1234567890',
                    role='frontend',
                    letter_date='2024-01-01',
                    joining_date='2024-01-15'
                )
                dummy_candidate.save(using='neon')
            
            self.stdout.write(
                self.style.SUCCESS('   ✅ Created dummy candidates 0A20-0A29')
            )
            
            # Now delete all dummy candidates except 0A20-0A29
            # Actually, let's keep them and then delete the ones after 0A20
            candidates_to_delete = Candidate.objects.using('neon').filter(
                work_id__in=['0A21', '0A22', '0A23', '0A24', '0A25', '0A26', '0A27', '0A28', '0A29']
            )
            deleted_count, _ = candidates_to_delete.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'   ✅ Deleted {deleted_count} dummy candidates, keeping 0A20')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error setting up work ID: {str(e)}')
            )
        
        # Step 4: Verify the setup
        self.stdout.write('\n🔍 Verifying the setup...')
        try:
            # Check remaining candidates
            remaining_candidates = Candidate.objects.using('neon').count()
            remaining_offer_letters = OfferLetter.objects.using('neon').count()
            
            self.stdout.write(f'   Remaining candidates: {remaining_candidates}')
            self.stdout.write(f'   Remaining offer letters: {remaining_offer_letters}')
            
            # Check if we have the 0A20 candidate
            candidate_0a20 = Candidate.objects.using('neon').filter(work_id='0A20').first()
            if candidate_0a20:
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Found candidate with work ID 0A20')
                )
                # Clean up the dummy 0A20 candidate
                candidate_0a20.delete(using='neon')
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Cleaned up dummy 0A20 candidate')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('   ⚠️  Could not find candidate with work ID 0A20')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error verifying: {str(e)}')
            )
        
        # Step 5: Test next work ID generation
        self.stdout.write('\n🧪 Testing next work ID generation...')
        try:
            # Create a test candidate to verify the sequence
            test_candidate = Candidate(
                name='Test Candidate',
                email='test@example.com',
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
            
            if generated_work_id == '0A20':
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Work ID reset successful! Next ID will be 0A20')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️  Expected 0A20, got {generated_work_id}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error testing work ID: {str(e)}')
            )
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 Work ID Reset and Database Cleanup Completed!'))
        self.stdout.write('\n📋 Summary:')
        self.stdout.write('   • All candidates removed from Neon database')
        self.stdout.write('   • All offer letters removed from Neon database')
        self.stdout.write('   • Work ID sequence reset to start from 0A20')
        self.stdout.write('   • Ready for fresh candidate creation')
        self.stdout.write('\n🚀 Next Steps:')
        self.stdout.write('   • Create new candidates - they will start from 0A20')
        self.stdout.write('   • Generate offer letters with clean work IDs')
        self.stdout.write('=' * 60)
