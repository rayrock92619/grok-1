import os
import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def scrape_linkedin(keywords, location):
    print(f"Searching LinkedIn for {keywords} in {location}...")
    # Using the Guest Job Search API endpoint
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('li')
        
        leads = []
        for job in jobs[:5]: # Get top 5 jobs
            title = job.find('h3', class_='base-search-card__title')
            company = job.find('h4', class_='base-search-card__subtitle')
            link = job.find('a', class_='base-card__full-link')
            
            if title and company and link:
                leads.append(f"{title.text.strip()} at {company.text.strip()}\nLink: {link['href']}\n")
        
        return "\n".join(leads) if leads else "No LinkedIn jobs found."
    except Exception as e:
        return f"LinkedIn Scrape Error: {e}"

def send_email(content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'Sherlock Job Report: LinkedIn + Google'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return "Intelligence report emailed successfully!"
    except Exception as e:
        return f"Email dispatch failed: {e}"

if __name__ == "__main__":
    # You can change these keywords to match your "Senior Stack" interests
    linkedin_leads = scrape_linkedin("Software Developer", "United States")
    
    full_report = f"--- LINKEDIN LEADS ---\n\n{linkedin_leads}"
    print(full_report)
    
    status = send_email(full_report)
    print(status)
if __name__ == "__main__":
    # Targeting your specific expertise
    keywords = "DevOps Engineer Remote"
    location = "United States"
    
    linkedin_leads = scrape_linkedin(keywords, location)
    
    # Adding a timestamp so you know exactly when the hunt happened
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    full_report = f"--- SHERLOCK INTELLIGENCE REPORT: {now} ---\n\n"
    full_report += f"TARGET: {keywords}\n\n"
    full_report += f"--- LINKEDIN LEADS ---\n\n{linkedin_leads}"
    
    print(full_report)
    
    status = send_email(full_report)
    print(status)
