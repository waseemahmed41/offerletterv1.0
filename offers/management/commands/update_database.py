from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from offers.models import Template
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Update database with new templates and create users'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Starting database update...')
        
        # Clear existing templates
        self.stdout.write('🗑️  Clearing existing templates...')
        Template.objects.all().delete()
        
        # Template mappings
        template_mappings = [
            {
                'filename': 'frontend_offer_letter_template.docx',
                'name': 'Frontend Developer Template',
                'role': 'frontend'
            },
            {
                'filename': 'backend_offer_letter_template.docx',
                'name': 'Backend Developer Template',
                'role': 'backend'
            },
            {
                'filename': 'full_stack_offer_letter_template.docx',
                'name': 'Full Stack Developer Template',
                'role': 'full_stack'
            },
            {
                'filename': 'ml_developer_offer_letter_template.docx',
                'name': 'Machine Learning Engineer Template',
                'role': 'machine_learning'
            },
            {
                'filename': 'ui_ux_designer_offer_letter_template.docx',
                'name': 'UI/UX Designer Template',
                'role': 'ui_ux'
            },
            {
                'filename': 'digital_marketing_offer_letter_template.docx',
                'name': 'Digital Marketing Template',
                'role': 'digital_marketing'
            },
            {
                'filename': 'PR_offer_letter_template.docx',
                'name': 'PR Specialist Template',
                'role': 'pr'
            },
            {
                'filename': 'content_video_creator_offer_letter_template.docx',
                'name': 'Content Writer Template',
                'role': 'content'
            },
            {
                'filename': 'video_editor_offer_letter_template.docx',
                'name': 'Video Editor Template',
                'role': 'video_editor'
            },
            {
                'filename': 'RnD_offer_letter_template.docx',
                'name': 'R&D Specialist Template',
                'role': 'rnd'  # New role
            }
        ]
        
        # Add templates
        templates_dir = 'media/templates'
        created_count = 0
        
        for mapping in template_mappings:
            filepath = os.path.join(templates_dir, mapping['filename'])
            
            if os.path.exists(filepath):
                try:
                    template = Template.objects.create(
                        name=mapping['name'],
                        role=mapping['role'],
                        file=f'templates/{mapping["filename"]}',
                        is_active=True
                    )
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Created: {template.name} ({template.get_role_display()})')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error creating {mapping["name"]}: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  File not found: {filepath}')
                )
        
        self.stdout.write(f'\n📊 Templates created: {created_count}')
        
        # Create users
        self.stdout.write('\n👥 Creating users...')
        
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@thome.co.in',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'hr_manager',
                'email': 'hr.manager@thome.co.in',
                'first_name': 'HR',
                'last_name': 'Manager',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'recruiter',
                'email': 'recruiter@thome.co.in',
                'first_name': 'Recruiter',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'hr_executive',
                'email': 'hr.executive@thome.co.in',
                'first_name': 'HR',
                'last_name': 'Executive',
                'is_staff': True,
                'is_superuser': False
            }
        ]
        
        created_users = 0
        
        for user_data in users_data:
            username = user_data['username']
            
            # Check if user exists
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                # Update existing user
                for key, value in user_data.items():
                    if key != 'password':
                        setattr(user, key, value)
                user.save()
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Updated existing user: {username}')
                )
            else:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    email=user_data['email'],
                    password='Temp@123456',  # Default password
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_staff=user_data['is_staff'],
                    is_superuser=user_data['is_superuser']
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created user: {username} (Password: Temp@123456)')
                )
                created_users += 1
        
        self.stdout.write(f'\n👥 Users created: {created_users}')
        
        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 Database update completed!'))
        self.stdout.write('\n📋 Summary:')
        self.stdout.write(f'   • Templates: {created_count} created')
        self.stdout.write(f'   • Users: {created_users} created')
        self.stdout.write('\n🔑 Default passwords: Temp@123456')
        self.stdout.write('⚠️  Please change passwords after first login!')
        self.stdout.write('='*50)
