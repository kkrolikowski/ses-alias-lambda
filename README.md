# ses-alias-lambda
Lambda is designed to send raw emails through AWS Simple Email Services.

## How it works
The Lambda function is invoked by the SES service and receives an event containing information about the sender and the MessageID. The MessageID is required to locate the corresponding object with the raw email message in the S3 bucket. Based on the recipient address received in the event, email alias targets are located in the AWS SSM Parameter Store service.

### Environment variables

| Variable | Description |
| ---------| ------------|
| EMAIL_BUCKET | S3 bucket name with raw email objects |
| ALIAS_MAP_PARAM | SSM parameter path with email alias mappings |

