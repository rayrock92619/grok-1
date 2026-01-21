import os
import smtplib
import requests
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Get secrets from .env
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(job_leads):
    msg = EmailMessage()
    msg.set_content(job_leads)
    msg['Subject'] = 'New Job Leads for Ray'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER # Sending it to yourself

    try:
        # Using Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Email failed: {e}"

def scrape_jobs():
    print("Searching for jobs...")
    return "Here are your jobs: Software Developer position in Android dev..."

if __name__ == "__main__":
    leads = scrape_jobs()
    status = send_email(leads)
    print(status)
