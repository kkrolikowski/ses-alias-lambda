import os

from lib.bucket import get_email_body
from lib.mailparser import prepare_email_message
from lib.params import get_alias_mappings
from lib.sendmail import send_mail

def lambda_handler(event, context):
  bucket_name = os.environ['EMAIL_BUCKET']
  param_name = os.environ['ALIAS_MAP_PARAM']

  for record in event['Records']:
    object_key = record['ses']['mail']['messageId']
    email_alias = record['ses']['mail']['destination'][0]
    print(f"Received email for alias {email_alias}")
    
    # Get the target email addresses for the alias
    targets = get_alias_mappings(param_name, email_alias)

    # Fetch raw email from S3
    raw_email = get_email_body(bucket_name, object_key)

    # Prepare and send email
    maildata = prepare_email_message(raw_email, targets)
    response = send_mail(maildata)
    if response.get('MessageId'):
      print(f"Email sent: {response['MessageId']}")
    else:
      print(f"Error sending email: {response}")
