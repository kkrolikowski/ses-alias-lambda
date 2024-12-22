import boto3
from email.parser import BytesHeaderParser
from email.mime.multipart import MIMEMultipart
from email import policy

from lib.helpers import mail_address_helper

def send_mail(maildata: MIMEMultipart) -> dict:
  """
  Send an email using the AWS SES service.
  maildata: MIMEMultipart: The email message to send.
  Returns: dict: The response from the send_raw_email API call.
  """
  ses = boto3.client('ses')

  try:
    parser = BytesHeaderParser(policy=policy.default)
    mimedata = parser.parsebytes(maildata.as_bytes())

    source = mail_address_helper(mimedata["From"])
    destinations = mail_address_helper(mimedata["To"]).split(",")

    print(f"Sending email from {source} to: {", ".join(str(el) for el in destinations)}")

    response = ses.send_raw_email(
      Source=source,
      Destinations=destinations,
      RawMessage={
        "Data": maildata.as_bytes()
      }
    )
    return response
  except Exception as e:
    print(f"Error sending email: {e}")
  return None