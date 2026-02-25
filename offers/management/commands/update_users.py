from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Remove existing users and add new users to both SQLite and Neon databases'

    def handle(self, *args, **options):
        common_password = 'OL@thome999'
        
        # New users data
        users_data = [
            {
                'username': 'pratheek@thome',
                'email': 'pratheek.reddy@thome.co.in',
                'first_name': 'Pratheek',
                'last_name': 'Reddy',
                'is_staff': True,
                'is_superuser': True  # Make Pratheek admin
            },
            {
                'username': 'ravinder@thome',
                'email': 'ravinder.reddy@thome.co.in',
                'first_name': 'Ravinder',
                'last_name': 'Reddy',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'revanth@thome',
                'email': 'arimillirevanth@gmail.com',
                'first_name': 'Revanth',
                'last_name': 'Arimilli',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'waseem@thome',
                'email': 'mdwaseemahmed156@gmail.com',
                'first_name': 'Waseem',
                'last_name': 'Ahmed',
                'is_staff': True,
                'is_superuser': False
            }
        ]
        
        # Process both databases
        databases = ['default', 'neon']
        
        for db in databases:
            db_name = 'SQLite' if db == 'default' else 'Neon PostgreSQL'
            self.stdout.write(f'\n🔄 Processing {db_name} Database...')
            self.stdout.write('=' * 50)
            
            # Remove existing users
            existing_count = User.objects.using(db).count()
            self.stdout.write(f'🗑️  Removing {existing_count} existing users from {db_name}...')
            User.objects.using(db).all().delete()
            
            # Add new users
            created_count = 0
            for user_data in users_data:
                try:
                    user = User(
                        username=user_data['username'],
                        email=user_data['email'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_staff=user_data['is_staff'],
                        is_superuser=user_data['is_superuser']
                    )
                    user.set_password(common_password)
                    user.save(using=db)
                    created_count += 1
                    
                    role = 'Admin' if user_data['is_superuser'] else 'Staff'
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Created {role}: {user_data["username"]} ({user_data["email"]})'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Error creating user {user_data["username"]}: {str(e)}'
                        )
                    )
            
            self.stdout.write(f'\n📊 {db_name} Summary:')
            self.stdout.write(f'   • Users created: {created_count}')
            self.stdout.write(f'   • Common password: {common_password}')
        
        # Final summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 User Update Completed Successfully!'))
        self.stdout.write('\n📋 Final Summary:')
        self.stdout.write('   • 4 users added to both SQLite and Neon databases')
        self.stdout.write('   • All existing users removed')
        self.stdout.write(f'   • Common password: {common_password}')
        self.stdout.write('\n👥 User Details:')
        
        for user_data in users_data:
            role = 'Admin' if user_data['is_superuser'] else 'Staff'
            self.stdout.write(f'   • {user_data["username"]} - {role} - {user_data["email"]}')
        
        self.stdout.write('\n🔑 Login Credentials:')
        self.stdout.write(f'   • Username: Use any of the 4 usernames above')
        self.stdout.write(f'   • Password: {common_password}')
        self.stdout.write('\n⚠️  Important Notes:')
        self.stdout.write('   • Pratheek is the admin user (superuser)')
        self.stdout.write('   • Others are staff users with limited access')
        self.stdout.write('   • Change passwords after first login for security')
        self.stdout.write('=' * 60)
