import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIGURATION
JENKINS_URL = "http://43.205.236.88:8080"
USERNAME = "admin"
API_TOKEN = "11e261addeb391a613e8b86994fdec9171"
JOB_NAME = "CI_Job"

# Email Configuration
EMAIL_FROM = "venkyy82@gmail.com"
EMAIL_PASSWORD = "bjwf ldik azsp cigt"  # Your app password (keep it safe!)
EMAIL_TO = "venkyy82@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_last_build_number():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))
    response.raise_for_status()
    data = response.json()
    last_build = data.get('lastBuild')
    if last_build is None:
        raise ValueError("No builds found for this job.")
    return last_build['number']

def get_build_status(build_number):
    url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/api/json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))
    response.raise_for_status()
    data = response.json()
    return data.get('result')

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    try:
        build_number = get_last_build_number()
        status = get_build_status(build_number)
        message = (
            f"Job Name: {JOB_NAME}\n"
            f"Last Build Number: {build_number}\n"
            f"Status: {status}"
        )
        print(message)
        send_email(f"Jenkins Build Status for {JOB_NAME}", message)
    except Exception as e:
        print(f"Error: {e}")
        send_email(f"Jenkins Build Status - ERROR for {JOB_NAME}", str(e))

if __name__ == "__main__":
    main()
