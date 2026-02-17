# mailer.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


def _send_email(subject: str, html_body: str):
    """Core email sending function using SMTP"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Haram Umrah Travels <{Config.SMTP_EMAIL}>"
    msg["To"] = Config.ADMIN_EMAIL

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
        server.sendmail(Config.SMTP_EMAIL, Config.ADMIN_EMAIL, msg.as_string())

    print(f"[EMAIL SENT] {subject} → {Config.ADMIN_EMAIL}")


def send_inquiry_email(data: dict):
    """Send comprehensive package inquiry form data to admin"""
    
    # Calculate total travelers
    adults = int(data.get('adults', 1))
    children = int(data.get('children', 0))
    infants = int(data.get('infants', 0))
    total_travelers = adults + children + infants
    
    # Ramadan discount badge
    discount_badge = ""
    if data.get('ramadanDiscount'):
        discount_badge = """
        <div style="background: linear-gradient(135deg, #c9a84c, #e8c86d); color: #1a3c2a; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
            <strong>🌙 RAMADAN SPECIAL — 5% DISCOUNT APPLICABLE</strong>
        </div>
        """
    
    subject = f"New Umrah Inquiry — {data.get('fullName', 'Unknown')} ({data.get('packageTier', '').upper()})"

    html = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 650px; margin: 0 auto; background: #ffffff;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #1a3c2a, #0f2318); padding: 32px; text-align: center;">
            <h1 style="color: #c9a84c; margin: 0; font-size: 24px; font-weight: 700;">New Umrah Package Inquiry</h1>
            <p style="color: rgba(255,255,255,0.6); margin: 8px 0 0; font-size: 14px;">Haram Umrah Travels</p>
        </div>
        
        <!-- Content -->
        <div style="padding: 32px;">
            {discount_badge}
            
            <!-- Personal Information -->
            <div style="margin-bottom: 24px;">
                <h2 style="color: #1a3c2a; font-size: 16px; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 2px solid #c9a84c;">
                    👤 Personal Information
                </h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 10px 0; color: #666; width: 40%;">Full Name</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('fullName', '-')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Email</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('email', '-')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Phone</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('phone', '-')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">WhatsApp</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('whatsapp', data.get('phone', '-'))}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Preferred Contact</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('preferredContact', '-').replace('_', ' ').title()}</td>
                    </tr>
                </table>
            </div>
            
            <!-- Travel Information -->
            <div style="margin-bottom: 24px;">
                <h2 style="color: #1a3c2a; font-size: 16px; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 2px solid #c9a84c;">
                    ✈️ Travel Information
                </h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 10px 0; color: #666; width: 40%;">Departure City</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('departureCity', '-')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Travel Month</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('travelMonth', '-')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Departure Date</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('departureDate', '-')}</td>
                    </tr>
                </table>
            </div>
            
            <!-- Package & Group -->
            <div style="margin-bottom: 24px;">
                <h2 style="color: #1a3c2a; font-size: 16px; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 2px solid #c9a84c;">
                    🏨 Package & Group Details
                </h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 10px 0; color: #666; width: 40%;">Package Tier</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">
                            <span style="background: #1a3c2a; color: #c9a84c; padding: 4px 12px; border-radius: 20px; font-size: 12px;">
                                {data.get('packageTier', '-').upper()}
                            </span>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Room Type</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('roomType', '-').title()}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Adults</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{adults}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Children (2-12)</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{children}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Infants (&lt;2)</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{infants}</td>
                    </tr>
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 12px 10px; color: #1a3c2a; font-weight: 600;">Total Travelers</td>
                        <td style="padding: 12px 10px; font-weight: 700; color: #1a3c2a; font-size: 18px;">{total_travelers}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Elderly (65+)</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{'Yes' if data.get('hasElderly') else 'No'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Special Assistance</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('specialAssistance') or 'None specified'}</td>
                    </tr>
                </table>
            </div>
            
            <!-- Additional Services -->
            <div style="margin-bottom: 24px;">
                <h2 style="color: #1a3c2a; font-size: 16px; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 2px solid #c9a84c;">
                    ✨ Additional Services
                </h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 10px 0; color: #666; width: 40%;">Ziyarat Tours</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('ziyarat') or 'Not specified'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Visa Assistance</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('visaAssistance') or 'Not specified'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #666;">Travel Insurance</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #1a3c2a;">{data.get('travelInsurance') or 'Not specified'}</td>
                    </tr>
                </table>
            </div>
            
            <!-- Special Requests -->
            {'<div style="margin-bottom: 24px;"><h2 style="color: #1a3c2a; font-size: 16px; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 2px solid #c9a84c;">📝 Special Requests</h2><p style="background: #f8f9fa; padding: 16px; border-radius: 8px; color: #333; margin: 0; line-height: 1.6;">' + data.get('specialRequests', '') + '</p></div>' if data.get('specialRequests') else ''}
        </div>
        
        <!-- Footer -->
        <div style="background: #1a3c2a; padding: 20px; text-align: center;">
            <p style="color: rgba(255,255,255,0.6); margin: 0; font-size: 12px;">© Haram Umrah Travels — haramumrahtravels.com</p>
        </div>
    </div>
    """

    _send_email(subject, html)


def send_contact_email(data: dict):
    """Send general contact message to admin"""
    subject = f"New Contact Message — {data.get('fullName', 'Unknown')}"

    html = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #1a3c2a, #0f2318); padding: 24px; text-align: center;">
            <h1 style="color: #c9a84c; margin: 0; font-size: 22px;">New Contact Message</h1>
            <p style="color: rgba(255,255,255,0.6); margin: 8px 0 0; font-size: 14px;">Haram Umrah Travels</p>
        </div>
        <div style="padding: 24px; background: #f9f9f9;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee; width: 30%;">Name</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('fullName', '-')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee;">Email</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('email', '-')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee;">Phone</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('phone', '-')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; vertical-align: top;">Message</td>
                    <td style="padding: 10px 12px;">{data.get('message', '-')}</td>
                </tr>
            </table>
        </div>
        <div style="background: #1a3c2a; padding: 16px; text-align: center;">
            <p style="color: rgba(255,255,255,0.6); margin: 0; font-size: 12px;">© Haram Umrah Travels — info@haramumrahtravels.com</p>
        </div>
    </div>
    """

    _send_email(subject, html)