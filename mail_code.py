import smtplib
from email.message import EmailMessage

import json
# load  configuration JSON 
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


def send_mail(row_data):
    # Define email sender and recipient
    sender_email = config.get('email_id')
    password = config.get('email_password')

    receiver_email = row_data[2]

    # Set up the SMTP server (Gmail in this case)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create an EmailMessage object
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Webiste application " + row_data[3]
    # Set the email content (plain text)
    if row_data[3] == "Accepted":
        msg.set_content(f"Thank you for your response for {row_data[0]}, website: {row_data[1]}. We’re happy to inform you that you’ve successfully met the criteria and have been accepted. We appreciate your continued engagement with our company.")
    elif row_data[3] == "Denied":
        msg.set_content(f"Thank you for your response for {row_data[0]}, website: {row_data[1]}. We regret to inform you the website doesnt meet the requirements. We appreciate your understanding.")
    else:
        return False

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Log in to the server
        server.send_message(msg)  # Send the email message
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()  # Close the server connection

    return True