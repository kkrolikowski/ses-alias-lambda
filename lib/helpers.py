import re

def mail_address_helper(email: str) -> str:
  """
  Helper function to extract the barebone email address from an email header.
  email: str: The email header containing the email address.
  Returns: str: The email address.
  """

  # If the email address is already in the correct format, return it
  if '<' not in email:
    return email
  
  # Extract the email address from the header
  match = re.search("<(.+)>", email)
  email_clear = match.group(0)
  return re.sub(r"[<>]","", email_clear)

def safe_decode(payload, charset='utf-8'):
  """
  Safely decode text using the given charset.
  If decoding fails, it uses the default charset latin-1.
  payload: bytes: The text to decode.
  charset: str: The character encoding.
  Returns: str: The decoded text.
  """
  
  try:
    return payload.decode(charset)
  except (UnicodeDecodeError, LookupError):
    return payload.decode('latin-1')  # Fallback to latin-1 if decoding fails