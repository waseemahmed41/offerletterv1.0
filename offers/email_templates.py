"""
Email templates for offer letter notifications
"""

def get_offer_letter_email_content(candidate, company_name="Your Company"):
    """
    Generate beautiful HTML email content for offer letter
    """
    
    subject = f"🎉 Exciting Opportunity: Offer Letter - {candidate.role} at {company_name}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>T-HOME Offer Letter</title>
    </head>

    <body style="margin:0; padding:0; background-color:#F4F7FB; font-family:Segoe UI, Arial, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#F4F7FB; padding:30px 0;">
    <tr>
    <td align="center">

    <!-- Main Container -->
    <table width="650" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 8px 25px rgba(0,0,0,0.08);">

    <!-- Header -->
    <tr>
    <td style="background:linear-gradient(135deg,#1F3C68,#162C4E); padding:40px 30px; text-align:center;">

    <h1 style="color:#FFFFFF; margin:0; font-size:26px; letter-spacing:1px;">
    Congratulations
    </h1>

    <p style="color:#E2C15A; margin-top:10px; font-size:15px;">
    You've received an official offer from T-HOME
    </p>

    </td>
    </tr>

    <!-- Gold Divider -->
    <tr>
    <td style="height:4px; background:#C9A227;"></td>
    </tr>

    <!-- Content -->
    <tr>
    <td style="padding:45px 40px; color:#2C3E50; font-size:15px; line-height:1.7;">

    <p style="font-size:20px; font-weight:600; margin-top:0;">
    Dear <span style="color:#1F3C68;">{candidate.name}</span>,
    </p>

    <p>
    We are delighted to extend to you an offer for position of 
    <strong style="color:#1F3C68;">{candidate.role}</strong> at T-HOME.
    Your expertise and experience align perfectly with our mission of delivering innovative and trusted fintech solutions.
    </p>

    <p>
    Below is a summary of your employment details. The complete offer letter is attached to this email.
    </p>

    <!-- Offer Box -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#F4F7FB; border-left:5px solid #C9A227; padding:20px; margin:30px 0; border-radius:6px;">

    <tr>
    <td style="padding:10px 0; border-bottom:1px solid #E2C15A;">
    <span style="color:#6C7A89; font-weight:600;">Work ID:</span>
    <span style="float:right; font-weight:700; color:#C9A227;">{candidate.work_id}</span>
    </td>
    </tr>

    <tr>
    <td style="padding:10px 0; border-bottom:1px solid #E2C15A;">
    <span style="color:#6C7A89; font-weight:600;">Position:</span>
    <span style="float:right; font-weight:600;">{candidate.role}</span>
    </td>
    </tr>

    <tr>
    <td style="padding:10px 0; border-bottom:1px solid #E2C15A;">
    <span style="color:#6C7A89; font-weight:600;">Email:</span>
    <span style="float:right;">{candidate.email}</span>
    </td>
    </tr>

    <tr>
    <td style="padding:10px 0; border-bottom:1px solid #E2C15A;">
    <span style="color:#6C7A89; font-weight:600;">Phone:</span>
    <span style="float:right;">{candidate.phone}</span>
    </td>
    </tr>

    <tr>
    <td style="padding:10px 0;">
    <span style="color:#6C7A89; font-weight:600;">Joining Date:</span>
    <span style="float:right; font-weight:600; color:#1F3C68;">{candidate.joining_date.strftime('%d %B %Y')}</span>
    </td>
    </tr>

    </table>

    <!-- IMPORTANT ATTACHMENT NOTICE -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#FFF8E1; border:1px solid #C9A227; border-radius:8px; padding:20px; margin:30px 0;">
    <tr>
    <td style="text-align:center; color:#1F3C68;">

    <p style="margin:0; font-weight:700; font-size:16px; color:#C9A227;">
    Important
    </p>

    <p style="margin:10px 0 0 0; font-size:14px;">
    Please review the attached Offer Letter carefully. Kindly go through all terms and conditions before confirming your response.
    </p>
    
    <p style="margin:10px 0 0 0; font-size:14px;">
    Please send back the signed offer letter before your joining date.
    </p>

    </td>
    </tr>
    </table>

    <p>
    We look forward to welcoming you to T-HOME family and building a successful future together.
    </p>

    <p style="margin-top:30px;">
    Warm Regards,<br>
    <strong style="color:#1F3C68;">T-Home Careers</strong>
    </p>

    </td>
    </tr>

    <!-- Footer -->
    <tr>
    <td style="background:#162C4E; padding:25px; text-align:center; color:#FFFFFF; font-size:13px;">

    <p style="margin:5px 0;">
    © 2026 <span style="color:#C9A227; font-weight:600;">T-HOME</span> | Your Trusted Partner
    </p>

    <p style="margin:5px 0; opacity:0.8;">
    This is an automated message from T-Home Careers
    </p>

    </td>
    </tr>

    </table>

    </td>
    </tr>
    </table>

    </body>
    </html>
    """
    
    # Plain text version for email clients that don't support HTML
    text_content = f"""
    Congratulations {candidate.name}!
    
    We are delighted to extend to you an offer for the position of {candidate.role} at T-HOME. Your expertise and experience align perfectly with our mission of delivering innovative and trusted fintech solutions.
    
    Below is a summary of your employment details. The complete offer letter is attached to this email.
    
    Offer Details:
    - Work ID: {candidate.work_id}
    - Position: {candidate.role}
    - Email: {candidate.email}
    - Phone: {candidate.phone}
    - Joining Date: {candidate.joining_date.strftime('%d %B %Y')}
    
    Please review the attached Offer Letter carefully. Kindly go through all terms and conditions before confirming your response.
    
    We look forward to welcoming you to T-HOME family and building a successful future together.
    
    Warm Regards,
    T-Home Careers
    """
    
    return {
        'subject': subject,
        'html_content': html_content,
        'text_content': text_content
    }

def get_bulk_upload_confirmation_email_content(success_count, error_count, company_name="Your Company"):
    """
    Generate email content for bulk upload confirmation
    """
    
    subject = f"📊 Bulk Upload Summary - {success_count} Candidates Processed"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bulk Upload Summary - {company_name}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            
            .container {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }}
            
            .stat-box {{
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }}
            
            .success {{
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }}
            
            .error {{
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }}
            
            .footer {{
                background: #2c3e50;
                color: white;
                padding: 30px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Bulk Upload Complete</h1>
                <p>Your candidate upload has been processed</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stat-box success">
                        <h3>✅ {success_count}</h3>
                        <p>Successfully Uploaded</p>
                    </div>
                    <div class="stat-box error">
                        <h3>⚠️ {error_count}</h3>
                        <p>Errors Encountered</p>
                    </div>
                </div>
                
                <p>Log in to your dashboard to view the uploaded candidates and generate offer letters.</p>
            </div>
            
            <div class="footer">
                <p>{company_name} HR System</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return {
        'subject': subject,
        'html_content': html_content,
        'text_content': f"Bulk upload complete. {success_count} candidates uploaded successfully, {error_count} errors."
    }
