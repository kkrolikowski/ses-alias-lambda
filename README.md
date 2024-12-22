# ses-alias-lambda

Lambda is designed to send raw emails through AWS Simple Email Services.

## How it works

The Lambda function is invoked by the SES service and receives an event containing information about the sender and the MessageID. The MessageID is required to locate the corresponding object with the raw email message in the S3 bucket. Based on the recipient address received in the event, email alias targets are located in the AWS SSM Parameter Store service.

### Environment variables

| Variable        | Description                                  |
| --------------- | -------------------------------------------- |
| EMAIL_BUCKET    | S3 bucket name with raw email objects        |
| ALIAS_MAP_PARAM | SSM parameter path with email alias mappings |

### Input data

The Lambda function is invoked by the AWS SES service.
Event fragment:

```json
{
  "eventSource": "aws:ses",
  "eventVersion": "1.0",
  "ses": {
    "mail": {
      "timestamp": "2024-12-19T20:09:07.988Z",
      "source": "sender@example.com",
      "messageId": "42psa7hk4n6m77qd56tum3dlhtnc3bnc6bhnaio1",
      "destination": ["alias@foo.com"],
      "headersTruncated": false,
      ...
```

From the event, the messageId and destination, which contains the alias address, are extracted. The messageId is also the key name in the S3 bucket containing the email content.

- The Lambda function retrieves the email content from the S3 bucket.
- It adjusts the email to meet SES requirements.
- Acquires mail alias targets from the SSM Parameter Store
- It sends the modified email to the recipients of the email alias.