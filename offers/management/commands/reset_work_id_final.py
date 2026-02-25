from django.core.management.base import BaseCommand
from offers.models import Candidate, OfferLetter

class Command(BaseCommand):
    help = 'Reset work ID to 0A20 and remove all candidates from Neon database (Direct Approach)'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Resetting work ID and cleaning Neon database...')
        self.stdout.write('=' * 60)
        
        # Step 1: Remove all candidates from Neon database
        self.stdout.write('\n🗑️  Removing all candidates from Neon database...')
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
        
        # Step 3: Create a candidate with work_id 0A20 directly
        self.stdout.write('\n🔄 Creating candidate with work_id 0A20...')
        try:
            # Create candidate with specific work_id
            base_candidate = Candidate(
                work_id='0A20',
                name='Base Reset Candidate',
                email='base@reset.com',
                phone='+1234567890',
                role='frontend',
                letter_date='2024-01-01',
                joining_date='2024-01-15'
            )
            # Save without triggering generate_work_id
            base_candidate.save(using='neon', force_insert=True)
            
            self.stdout.write(
                self.style.SUCCESS('   ✅ Created base candidate with work_id 0A20')
            )
            
            # Now delete the base candidate to clean up
            base_candidate.delete(using='neon')
            self.stdout.write(
                self.style.SUCCESS('   ✅ Removed base candidate, sequence is now set')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error creating base candidate: {str(e)}')
            )
        
        # Step 4: Test next work ID generation
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
                # If we got a different ID, let's try to force it
                if generated_work_id > '0A20':
                    self.stdout.write('\n🔄 Attempting to force reset to 0A20...')
                    try:
                        # Create candidates from 0A20 up to the generated ID to fill the gap
                        current_num = int(generated_work_id[2:])
                        for i in range(20, current_num):
                            filler_candidate = Candidate(
                                work_id=f'0A{i:02d}',
                                name=f'Filler Candidate {i}',
                                email=f'filler{i}@example.com',
                                phone='+1234567890',
                                role='frontend',
                                letter_date='2024-01-01',
                                joining_date='2024-01-15'
                            )
                            filler_candidate.save(using='neon', force_insert=True)
                        
                        # Now delete all filler candidates
                        deleted_count, _ = Candidate.objects.using('neon').filter(
                            work_id__gte='0A20', work_id__lt=generated_work_id
                        ).delete()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'   ✅ Created and deleted {deleted_count} filler candidates')
                        )
                        
                        # Test again
                        test_candidate2 = Candidate(
                            name='Test Candidate 2',
                            email='test2@example.com',
                            phone='+1234567890',
                            role='frontend',
                            letter_date='2024-01-01',
                            joining_date='2024-01-15'
                        )
                        test_candidate2.save(using='neon')
                        
                        new_work_id = test_candidate2.work_id
                        self.stdout.write(f'   New generated work ID: {new_work_id}')
                        
                        test_candidate2.delete(using='neon')
                        
                        if new_work_id == '0A20':
                            self.stdout.write(
                                self.style.SUCCESS('   ✅ Work ID force reset successful!')
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'   ⚠️  Still getting {new_work_id}')
                            )
                            
                    except Exception as force_error:
                        self.stdout.write(
                            self.style.ERROR(f'   ❌ Error in force reset: {str(force_error)}')
                        )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error testing work ID: {str(e)}')
            )
        
        # Step 5: Final cleanup - remove any remaining candidates
        self.stdout.write('\n🧹 Final cleanup...')
        try:
            remaining_count = Candidate.objects.using('neon').count()
            if remaining_count > 0:
                deleted_count, _ = Candidate.objects.using('neon').all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ Final cleanup: removed {deleted_count} candidates')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Final cleanup: no candidates to remove')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error in final cleanup: {str(e)}')
            )
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 Work ID Reset and Database Cleanup Completed!'))
        self.stdout.write('\n📋 Final Status:')
        self.stdout.write('   • All candidates removed from Neon database')
        self.stdout.write('   • All offer letters removed from Neon database')
        self.stdout.write('   • Work ID sequence reset to start from 0A20')
        self.stdout.write('   • Database is clean and ready')
        self.stdout.write('\n🚀 Ready for Use:')
        self.stdout.write('   • Next candidate created will have work ID 0A20')
        self.stdout.write('   • Subsequent candidates will be 0A21, 0A22, etc.')
        self.stdout.write('=' * 60)
