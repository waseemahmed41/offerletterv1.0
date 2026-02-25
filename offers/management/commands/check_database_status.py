from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from offers.models import Candidate, Template, OfferLetter

User = get_user_model()

class Command(BaseCommand):
    help = 'Check database status for both SQLite and Neon'

    def handle(self, *args, **options):
        self.stdout.write('📊 Database Status Report')
        self.stdout.write('=' * 60)
        
        databases = [
            ('default', 'SQLite (Local)'),
            ('neon', 'Neon PostgreSQL (Production)')
        ]
        
        for db_alias, db_name in databases:
            self.stdout.write(f'\n🗄️  {db_name}:')
            self.stdout.write('-' * 40)
            
            # Users
            user_count = User.objects.using(db_alias).count()
            self.stdout.write(f'   Users: {user_count}')
            
            # Templates
            template_count = Template.objects.using(db_alias).count()
            self.stdout.write(f'   Templates: {template_count}')
            
            # Candidates
            candidate_count = Candidate.objects.using(db_alias).count()
            self.stdout.write(f'   Candidates: {candidate_count}')
            
            # Offer Letters
            offer_letter_count = OfferLetter.objects.using(db_alias).count()
            self.stdout.write(f'   Offer Letters: {offer_letter_count}')
            
            # Recent users
            if user_count > 0:
                self.stdout.write('\n   Recent Users:')
                users = User.objects.using(db_alias).all()[:3]
                for user in users:
                    role = 'Admin' if user.is_superuser else 'Staff'
                    self.stdout.write(f'   • {user.username} ({role})')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('✅ Database status check completed!')
