import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import date

# ---------- CONFIGURATION ----------
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"   # Use App Password for Gmail
RECEIVER_EMAIL = "recipient@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ---------- EMAIL DETAILS ----------
subject = f"Automated Report - {date.today().strftime('%d %B %Y')}"
body = """
Hello Team,

Please find attached the latest report.

Best regards,
Automated Report Bot 🤖
"""

# ---------- ATTACHMENT ----------
file_path = "C:/Users/YourName/Documents/Weekly_Report.pdf"  # Change this path

# ---------- EMAIL CREATION ----------
msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))

# Attach file
if os.path.exists(file_path):
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(file_path)}",
    )
    msg.attach(part)
else:
    print("⚠️ Attachment file not found:", file_path)

# ---------- SEND EMAIL ----------
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    print("✅ Email sent successfully to", RECEIVER_EMAIL)
except Exception as e:
    print("❌ Failed to send email:", str(e))
finally:
    server.quit()
