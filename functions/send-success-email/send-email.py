import boto3
from botocore.exceptions import ClientError
import os
ses_client = boto3.client('ses')
def send_email(sender_email, recipient_email, subject, body_text, body_html):

    # Try to send the email
    try:
        # Provide the contents of the email
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    sender_email,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender_email,
        )
    except ClientError as e:
        # Print error message if the email could not be sent
        print(f"Email sending failed. Error message: {e.response['Error']['Message']}")
    else:
        print("Email sent successfully!")
        print("Message ID:", response['MessageId'])



def lambda_handler(event, context):
    try:
        sender_email = 'viswatejaster@gmail.com'
        recipient_email = 'viswatejaster@gmail.com'
        subject = 'MLOPs Model deployment Success'
        body_text = 'This is a test email sent from Amazon SES.'
        link_url= f"http://{os.environ['LOADBALANCER_NAME']}:{event['data']['port']}/health"
        print(link_url)
        link_text = "your endpoint"
        with open("email_template.html", "r") as f:
            html_body = f.read()
        with open("email_style.css", "r") as f:
            css_style = f.read()
        
        formatted_html = html_body.replace(
        "<p>replace</p>", f"<p>Here is your endpoint for inferencing: <a href=\"{link_url}\">{link_text}</a></p>")
    
        body_html = f"<html><head><style>{css_style}</style></head><body>{formatted_html}</body></html>"
    
        _ = send_email(sender_email, recipient_email, subject, body_text, body_html)
        return 200
    
    except Exception as err:
        
        return "error"
