# Offer Letter Automation System

A production-ready Django application for automating offer letter generation and distribution with professional UI/UX.

## 🚀 Features

### Core Functionality
- **Multi-Database Architecture**: SQLite for authentication, Neon PostgreSQL for candidate data
- **Professional 3D UI**: Modern glass-morphism design with Tailwind CSS
- **Bulk Upload**: CSV/Excel file import with validation and preview
- **Template Processing**: DOCX template placeholder replacement
- **Email Integration**: Automated offer letter delivery with attachments
- **Work ID Generation**: Automatic sequential ID assignment
- **Status Tracking**: Real-time candidate status updates

### User Interface
- **3D Login Page**: Professional authentication with floating animations
- **Interactive Dashboard**: Real-time statistics and recent activity
- **Candidate Management**: Advanced filtering and search capabilities
- **Popup Cards**: Detailed candidate preview with action buttons
- **Responsive Design**: Mobile-friendly interface

### Technical Features
- **Role-Based Access**: Admin, HR Manager, Recruiter roles
- **File Upload Validation**: Secure file handling with size limits
- **Error Handling**: Comprehensive error reporting and logging
- **AJAX Integration**: Smooth user experience without page reloads
- **Security**: CSRF protection, secure headers, input validation

## 📋 Requirements

- Python 3.8+
- Django 4.2.7
- PostgreSQL (Neon)
- Redis (for background tasks)
- LibreOffice (for DOCX processing)

## 🛠️ Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd offer-letter-automation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env` file and update with your settings:
```bash
cp .env.example .env
```

Update the following variables:
- `SECRET_KEY`: Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`: Neon PostgreSQL credentials
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Email configuration

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Default Users
```bash
python create_superuser.py
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## 👤 Default Credentials

### Admin User
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator

### HR Manager
- **Username**: hrmanager
- **Password**: hr123
- **Role**: HR Manager

## 📁 Project Structure

```
offer_letter_automation/
├── accounts/                 # User authentication and management
│   ├── models.py            # Custom User model
│   ├── views.py             # Login/Signup views
│   ├── forms.py             # Authentication forms
│   └── urls.py              # Account URLs
├── offers/                   # Core offer letter functionality
│   ├── models.py            # Candidate, Template, OfferLetter models
│   ├── views.py             # Dashboard, bulk upload, candidate management
│   ├── utils.py             # DOCX processing and email utilities
│   ├── admin.py             # Admin interface configuration
│   └── urls.py              # Offer URLs
├── templates/               # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── accounts/           # Authentication templates
│   └── offers/             # Dashboard and management templates
├── static/                  # CSS, JS, and static assets
├── media/                   # Uploaded files and generated documents
├── offer_automation/        # Django project settings
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## 📊 Database Schema

### Users Table (SQLite)
- Custom user model with role-based access
- Fields: username, email, role, phone, department

### Candidates Table (Neon PostgreSQL)
- Candidate information and status tracking
- Fields: work_id, name, email, phone, role, dates, status

### Templates Table
- DOCX template management
- Fields: name, file, is_active, created_by

### Offer Letters Table
- Generated offer letter tracking
- Fields: candidate, template, generated_file, sent_at

## 🔄 Workflow

1. **Login**: Users authenticate with role-based access
2. **Dashboard**: View statistics and recent candidates
3. **Bulk Upload**: Import candidates from CSV/Excel
4. **Preview**: Review candidate details in popup cards
5. **Generate**: Create offer letters using DOCX templates
6. **Send**: Email offer letters to candidates
7. **Track**: Monitor status and delivery

## 📧 Email Configuration

### Gmail SMTP Setup
1. Enable 2-factor authentication
2. Generate App Password
3. Update `.env` file:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

### SendGrid Alternative
1. Create SendGrid account
2. Generate API key
3. Update `.env` file:
   ```
   SENDGRID_API_KEY=your-sendgrid-api-key
   ```

## 📄 File Format for Bulk Upload

### Required Columns
- `name`: Full name of candidate
- `email`: Email address
- `phone`: Phone number
- `role`: Job position
- `letter_date`: Offer letter date (YYYY-MM-DD)
- `joining_date`: Joining date (YYYY-MM-DD)

### Example CSV
```csv
name,email,phone,role,letter_date,joining_date
John Doe,john@example.com,9876543210,Software Engineer,2024-02-15,2024-03-01
Jane Smith,jane@example.com,9876543211,Product Manager,2024-02-16,2024-03-15
```

## 🎨 DOCX Template Placeholders

Use these placeholders in your DOCX templates:
- `{{name}}`: Candidate full name
- `{{email}}`: Email address
- `{{phone}}`: Phone number
- `{{role}}`: Job position
- `{{letter_date}}`: Offer letter date
- `{{joining_date}}`: Joining date
- `{{work_id}}`: Generated work ID

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS`
3. Set up production database
4. Configure static file serving
5. Set up SSL/TLS

### Docker Deployment
```bash
docker build -t offer-automation .
docker run -p 8000:8000 offer-automation
```

## 🔧 Customization

### Adding New Roles
1. Update `ROLE_CHOICES` in `accounts/models.py`
2. Update permissions in views
3. Update UI role-specific features

### Custom Templates
1. Upload DOCX templates through admin
2. Use placeholder variables
3. Mark as active to use in generation

### Email Customization
1. Modify email templates in `offers/views.py`
2. Update subject lines and body content
3. Add custom attachments

## 🐛 Troubleshooting

### Common Issues
1. **Database Connection**: Check Neon PostgreSQL credentials
2. **Email Sending**: Verify SMTP settings and app passwords
3. **File Upload**: Check file size limits and permissions
4. **DOCX Processing**: Ensure LibreOffice is installed

### Debug Mode
Enable debug logging by setting `DEBUG=True` in `.env`

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django logs
3. Verify environment configuration
4. Test with sample data

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

**Built with ❤️ for HR Professionals**
