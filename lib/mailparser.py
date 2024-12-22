from email.parser import BytesParser
from email import policy
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from lib.helpers import mail_address_helper, safe_decode

def prepare_email_message(raw_email: bytes, targets: list) -> MIMEMultipart:
  '''
  Parse the raw email and prepare a new email message to be sent.
  raw_email: bytes - The raw email message
  targets: list - The list of email addresses to send the email to
  return: MIMEMultipart - The new email message
  '''
  
   #
  ### Objects needed to parse and create email message
   #

  # Object to parse incoming email
  mailObject = BytesParser(policy=policy.default)
  # Create a MIMEMultipart object to store the parsed email
  mainMSG = MIMEMultipart('mixed')
  relatedMSG = MIMEMultipart('related')
  alternativeMSG = MIMEMultipart('alternative')

  # Parse the raw email
  mail = mailObject.parsebytes(raw_email)
  
  # Define the content types that are considered binary
  binary_content_types = ['application', 'audio', 'video']

  header_to = ",".join(targets)

  # Set the basic headers of the email
  mainMSG["From"] = mail_address_helper(mail.get("To"))         # SES requires the From header to be the verified recipient
  mainMSG["To"] = header_to
  mainMSG["Reply-To"] = mail_address_helper(mail.get("From"))
  mainMSG["Subject"] = mail.get("Subject")

  # Loop through the parts of the email
  if mail.is_multipart():
    for part in mail.walk():
      # Skip the part if it has no payload
      if part.get_payload(decode=True) is None:
        continue

      # Add text and html parts to the new email message
      content_type = part.get_content_type()
      content_disposition = part.get_content_disposition()
      charset = part.get_content_charset() or 'utf-8'

      if content_type == 'text/html':
        html = safe_decode(part.get_payload(decode=True), charset)
        relatedMSG.attach(MIMEText(html, content_type.split('/')[1]))
      elif content_type == 'text/plain':
        text = safe_decode(part.get_payload(decode=True), charset)
        alternativeMSG.attach(MIMEText(text, content_type.split('/')[1]))
      
      elif content_disposition == 'inline' and content_type.startswith('image/'):
        filename = part.get_filename()
        content_id = part.get("Content-ID")
        if not content_id:
          # Generowanie unikalnego Content-ID, jeśli go brakuje
          content_id = filename or "image-" + str(hash(part.get_payload(decode=True)))
        
        # Usuń znaki specjalne, jeśli to potrzebne
        content_id = content_id.strip("<>")
        
        # Tworzenie MIMEImage z odpowiednimi nagłówkami
        image = MIMEImage(part.get_payload(decode=True), _subtype=content_type.split('/')[1])
        image.add_header('Content-ID', f'<{content_id}>')
        image.add_header('Content-Disposition', 'inline', filename=filename)

        # Dodaj obraz do wiadomości
        relatedMSG.attach(image)
      # Add attachments to the new email message
      elif content_disposition == 'attachment' or any([x in content_type for x in binary_content_types]):
        filename = part.get_filename()
        if filename:
          part.replace_header('Content-Disposition', f'attachment; filename="{filename}"')
        part.set_type('application/octet-stream')
        mainMSG.attach(part)
  else:
    # If the email is not multipart, add the text to the alternative message
    text = safe_decode(mail.get_payload(decode=True), mail.get_content_charset() or 'utf-8')
    if 'doctype html' in text.lower():
      relatedMSG.attach(MIMEText(text, 'html'))
    else:
      alternativeMSG.attach(MIMEText(text, 'plain'))
  # Attach the text and html parts to the alternative message
  alternativeMSG.attach(relatedMSG)
  mainMSG.attach(alternativeMSG)
  # Debug messsage
  return mainMSG