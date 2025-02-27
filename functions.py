import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from datetime import datetime, timedelta

def send_email(subject, body, to_email, from_email, from_password, smtp_server, smtp_port):
    def send():
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, from_password)

            # Send the email
            server.send_message(msg)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

    # Run the send function in a separate thread
    Thread(target=send).start()

def getId(tasks):
    if len(tasks) == 0:
        return 1
    else:
        return tasks[-1]["id"] + 1

def createTask(username, app, id, description, begin, expires):
    task = {"id":id, "description":description, "status":"pending", "begin":begin, "expires":expires}
    for userData in app.users["users"]:
        if userData["username"] == username:
            userData["tasks"].append(task)
            app.dumpData()
            return userData["tasks"]
        
def transformDate(date):
    if date == None:
        return None
    year, month, day = date.split('-')
    return f"{day}-{month}-{year}"

def is_tomorrow(day, month, year):
    # Get tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Check if the provided date matches tomorrow's date
    return tomorrow.day == day and tomorrow.month == month and tomorrow.year == year



