import boto3
import json

def get_alias_mappings(param_name: str, email_alias: str) -> list:
  """
  Retrieve email alias mappings from SSM parameter store.  
  param_name: The name of the SSM parameter containing the alias mappings.
  email_alias: The email alias to look up.
  """
  ssm = boto3.client('ssm')
  try:
    response = ssm.get_parameter(Name=param_name, WithDecryption=False)
    param_value = json.loads(response['Parameter']['Value'])
    alias_targets = param_value.get(email_alias, None)
    return alias_targets
  
  except ssm.exceptions.ParameterNotFound:
    print(f"Alias mapping not found for: {email_alias}")
  except Exception as e:
    print(f"Error retrieving alias mapping: {e}")