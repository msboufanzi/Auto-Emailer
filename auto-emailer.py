from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
import smtplib
from dotenv import load_dotenv
import os
import csv
import time
import threading
import queue

# Custom variables (change these)
file_path = 'docs/contacts.csv'
email_subject = 'Candidature pour un stage de fin d’études - Ingénierie de Développement d’Applications'

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Sending Controls
PAUSE_BETWEEN_MESSAGES = 30  # seconds between emails
TIMEOUT = 30  # SMTP timeout in seconds
MAX_CONNECTIONS = 5  # Parallel connections
RETRIES = 1  # Number of retries if failed
PAUSE_BETWEEN_ATTEMPTS = 2  # Delay between retries

# Language Enum
class Language(Enum):
    ENGLISH = 'EN'
    SPANISH = 'ES'
    FRENCH = 'FR'

def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        return list(csv.reader(file))

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def send_email(subject, body, recipient, attachments=[]):
    """Function to send an email to a single recipient."""
    for attempt in range(RETRIES + 1):
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = recipient
            msg['Subject'] = subject

            # Attach email body with UTF-8 encoding
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            for attachment in attachments:
                try:
                    with open(attachment, 'rb') as file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                        msg.attach(part)
                except Exception as e:
                    print(f'Failed to attach file {attachment}: {e}')

            with smtplib.SMTP('smtp.gmail.com', 587, timeout=TIMEOUT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                print(f'Email sent to {recipient}')
            return

        except Exception as e:
            print(f'Failed to send email to {recipient} (Attempt {attempt+1}/{RETRIES+1}): {e}')
            if attempt < RETRIES:
                time.sleep(PAUSE_BETWEEN_ATTEMPTS)

def format_email(body, name):
    # If name is empty, use the email address as the name
    if not name:
        return body.replace('[NAME]', '')
    return body.replace('[NAME]', name)

def get_attachments(directory):
    return [os.path.join(directory, filename) for filename in os.listdir(directory) if not filename.startswith('.')]

def process_contact(contact):
    """Process a single contact row with flexible format handling"""
    # Default values
    email = ""
    name = ""
    language = "FR"  # Default to English
    
    # Handle different CSV formats
    if len(contact) >= 1:
        email = contact[0]
    
    if len(contact) >= 2:
        name = contact[1]
    
    if len(contact) >= 4:  # Format: email, name, title, language
        language = contact[3]
    elif len(contact) >= 3:  # Format: email, name, language
        language = contact[2]
    
    return email, name, language

# Main
contacts = read_csv(file_path)
email_templates = {
    'EN': read_txt('docs/email_EN.txt'),  # ENGLISH
    'ES': read_txt('docs/email_ES.txt'),  # Spanish
    'FR': read_txt('docs/email_FR.txt')   # French
}
all_attachments = get_attachments('attachments')

# Queue for contacts
contact_queue = queue.Queue()
for contact in contacts:
    contact_queue.put(contact)

# Global lock for sending emails
send_lock = threading.Lock()

def worker():
    while not contact_queue.empty():
        contact = contact_queue.get()
        email, name, language = process_contact(contact)
        
        if '@' not in email:
            print(f'Invalid email address: {email}')
            continue

        # Get the appropriate template or default to French if language not found
        locale_body = email_templates.get(language, email_templates['FR'])

        # Use a lock to ensure only one email is sent at a time
        with send_lock:
            send_email(
                subject=email_subject,
                body=format_email(locale_body, name),
                recipient=email,
                attachments=all_attachments
            )
            # Respect the pause between emails
            time.sleep(PAUSE_BETWEEN_MESSAGES)

        contact_queue.task_done()

# Multi-threading for parallel processing (but only one email sent at a time)
def threaded_sending():
    threads = []
    for _ in range(MAX_CONNECTIONS):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Run the threaded sending function
threaded_sending()
