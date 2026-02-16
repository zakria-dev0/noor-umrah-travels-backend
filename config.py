import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # SMTP Configuration
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")           # Your sending email
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")      # App password (not regular password)
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")           # Admin receives all form emails

    # CORS - add your frontend URLs
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")