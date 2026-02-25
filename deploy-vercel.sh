#!/bin/bash

# Vercel Deployment Script for Django Offer Letter Automation

echo "🚀 Starting Vercel Deployment for Django Project..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if user is logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel..."
    vercel login
fi

# Create .env.production file for Vercel
echo "📝 Creating production environment file..."
cat > .env.production << EOF
# Django Configuration
DJANGO_SETTINGS_MODULE=offer_automation.settings_vercel
SECRET_KEY=your-production-secret-key-here
DEBUG=False
VERCEL=true

# Database Configuration (Neon PostgreSQL)
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=your-neon-password
DB_HOST=ep-your-host.neon.tech
DB_PORT=5432

# Email Configuration
SENDGRID_API_KEY=your-sendgrid-api-key
EMAIL_HOST=smtp.zoho.in
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=Your Name <your-email@domain.com>

# File Upload Settings
MAX_UPLOAD_SIZE=10485760
ALLOWED_UPLOAD_EXTENSIONS=csv,xlsx,xls,docx
EOF

echo "✅ Environment file created: .env.production"
echo "⚠️  Please update the values in .env.production with your actual credentials"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements-vercel.txt

# Run database migrations (if database is configured)
read -p "🗄️  Do you want to run database migrations? (y/n): " run_migrations
if [[ $run_migrations == "y" || $run_migrations == "Y" ]]; then
    echo "🔄 Running database migrations..."
    python manage.py migrate --settings=offer_automation.settings_vercel
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=offer_automation.settings_vercel

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Update environment variables in Vercel Dashboard"
echo "2. Test your deployed application"
echo "3. Set up custom domain (optional)"
echo "4. Configure monitoring and error tracking"
echo ""
echo "🌐 Your app should be available at: https://your-app-name.vercel.app"
