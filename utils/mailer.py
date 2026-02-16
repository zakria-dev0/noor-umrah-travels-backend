import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


def _send_email(subject: str, html_body: str):
    """Core email sending function using SMTP"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Noor Umrah Travels <{Config.SMTP_EMAIL}>"
    msg["To"] = Config.ADMIN_EMAIL

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
        server.sendmail(Config.SMTP_EMAIL, Config.ADMIN_EMAIL, msg.as_string())

    print(f"[EMAIL SENT] {subject} → {Config.ADMIN_EMAIL}")


def send_inquiry_email(data: dict):
    """Send package inquiry form data to admin"""
    subject = f"New {data.get('packageType', 'Umrah')} Inquiry — {data.get('fullName', 'Unknown')}"

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a3c2a; padding: 24px; text-align: center;">
            <h1 style="color: #c9a84c; margin: 0; font-size: 22px;">New Package Inquiry</h1>
            <p style="color: #ffffffaa; margin: 8px 0 0; font-size: 14px;">Noor Umrah Travels</p>
        </div>
        <div style="padding: 24px; background: #f9f9f9;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee; width: 40%;">Package Type</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('packageType', '-')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee;">Full Name</td>
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
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee;">Adults</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('adults', 0)}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee;">Children</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('children', 0)}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee;">Duration (Days)</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('duration', '-')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a; border-bottom: 1px solid #eee;">Hotel Type</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #eee;">{data.get('hotelType', '-')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 12px; font-weight: bold; color: #1a3c2a;">Total Travelers</td>
                    <td style="padding: 10px 12px;">{int(data.get('adults', 0)) + int(data.get('children', 0))}</td>
                </tr>
            </table>
        </div>
        <div style="background: #1a3c2a; padding: 16px; text-align: center;">
            <p style="color: #ffffffaa; margin: 0; font-size: 12px;">© Noor Umrah Travels — noorumrahtravels.co.uk</p>
        </div>
    </div>
    """

    _send_email(subject, html)


def send_contact_email(data: dict):
    """Send general contact message to admin"""
    subject = f"New Contact Message — {data.get('fullName', 'Unknown')}"

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a3c2a; padding: 24px; text-align: center;">
            <h1 style="color: #c9a84c; margin: 0; font-size: 22px;">New Contact Message</h1>
            <p style="color: #ffffffaa; margin: 8px 0 0; font-size: 14px;">Noor Umrah Travels</p>
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
            <p style="color: #ffffffaa; margin: 0; font-size: 12px;">© Noor Umrah Travels — noorumrahtravels.co.uk</p>
        </div>
    </div>
    """

    _send_email(subject, html)