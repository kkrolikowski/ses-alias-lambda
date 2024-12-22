import re

def mail_address_helper(email: str) -> str:
  """
  Helper function to extract the email address from an email header.
  """
  if '<' not in email:
    return email
  
  match = re.search("<(.+)>", email)
  email_clear = match.group(0)
  return re.sub(r"[<>]","", email_clear)

def safe_decode(payload, charset='utf-8'):
  """
  Bezpieczne dekodowanie tekstu z użyciem podanego kodowania.
  Jeśli dekodowanie nie powiedzie się, używa domyślnego kodowania latin-1.
  """
  
  try:
    return payload.decode(charset)
  except (UnicodeDecodeError, LookupError):
    return payload.decode('latin-1')  # Alternatywne kodowanie