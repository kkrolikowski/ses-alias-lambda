import boto3

def get_email_body(bucket_name: str, object_key: str) -> bytes:
  """
  Retrieve the raw email content from S3.
  bucket_name: The name of the S3 bucket.
  object_key: The key of the S3 object.
  return: The raw email content as bytes.
  """
  s3 = boto3.client('s3')

  try:
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(f"Error retrieving email from S3: {response}")
      return None

    if 'Body' not in response:
      print(f"Error retrieving email from S3: No body in response")
      return None
    
    if response['ContentLength'] == 0:
      print(f"Error retrieving email from S3: Empty body")
      return None
    
    return response['Body'].read()
  except Exception as e:
    print(f"Error retrieving email from S3: {e}")
    return None