# Auto Emailer

**Auto Emailer** is a Python-based script designed to automate sending personalized emails with optional attachments. This tool reads contact information from a CSV file, dynamically customizes email templates, and sends emails using an SMTP server (e.g., Gmail).

⚠️ **Use this tool responsibly.** This script is intended for legitimate purposes such as reaching out to clients, sending newsletters, or other lawful communication. Do not use it to send unsolicited emails or spam recipients.

## Features
- Read contact details from a CSV file.
- Dynamically customize email templates based on recipient information.
- Add multiple attachments to emails.
- Supports multilingual email templates (e.g., English, Spanish, French).
- Handles invalid email addresses gracefully by skipping them.
- Respects email sending limits with configurable pauses between emails.

## Gmail Sending Limits
- **Daily Limit:** 500 emails per day (for free Gmail accounts).
- **Per Message Limit:** Up to 100 recipients per email.
- **Rate Limit:** Sending too fast (e.g., hundreds of emails in a short time) may trigger temporary blocks.

## Setup

### 1. Set Up Python Virtual Environment
Create and activate a virtual environment to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Libraries
Install the necessary Python packages:

```bash
pip install python-dotenv
```

### 3. Configure Email Authentication
- Create an [App Password](https://myaccount.google.com/apppasswords) for your email account.
- This is more secure than using your account password.

### 4. Customize Environment Variables
Create a `.env` file in the project directory and add your credentials:

```ini
EMAIL_ADDRESS="your_email@gmail.com"
EMAIL_PASSWORD="your_app_password"
```

### 5. Prepare Your Files
#### Contact List:
- Create a CSV file with contact information (e.g., name, email, preferred language).
- Save this file in the `docs/` folder.

**Example CSV format:**

```csv
email,name,language
example1@example.com,John Doe,EN
example2@example.com,Jane Smith,FR
```

#### Attachments:
- Add any files you want to send as email attachments to the `attachments/` folder.
- The `.gitkeep` file will be ignored.

#### Email Templates:
- Create text files for each language you plan to support (e.g., `email_EN.txt`, `email_FR.txt`).
- Save these files in the `docs/` folder.

**Example template (email_EN.txt):**

```
Dear [NAME],

This is a sample email body.

Best regards,
Your Name
```

### 6. Run the Script
Execute the script to start sending emails:

```bash
python auto-emailer.py
```

## Folder Structure
```bash
auto-emailer/
├── attachments/      # Folder for all email attachments
├── docs/             # Folder for email templates and contact CSV
├── auto-emailer.py   # Main script
├── .env              # Environment variables
├── LICENSE           # Project license
├── README.md         # Documentation
```

## Responsibilities and Guidelines
- **Use responsibly:** Ensure you have the consent of your recipients before sending emails.
- **Respect privacy:** Avoid sharing or misusing recipient information.
- **Avoid spamming:** This script is not intended for sending unsolicited emails.

Misuse of this tool may violate laws such as the CAN-SPAM Act, GDPR, or other regulations in your jurisdiction.

## Contributions
Contributions are welcome! If you have suggestions for improvements, feel free to create an issue or submit a pull request.

## Support
If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/msboufanzi/Auto-Emailer).

