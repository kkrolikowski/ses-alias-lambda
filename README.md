# AWS SES Email Alias Lambda

This function helps solve a limitation of AWS Simple Email Service: you can’t send emails to external recipients using a FROM address that hasn’t been verified. The function disassembles the email and replaces the `FROM` address with an address from a domain verified in the SES service. It then reassembles all the parts and sends the email to the target recipients.


## How it works

The Lambda function is invoked by the SES service and receives an event containing information about the sender and the MessageID. The MessageID is required to locate the corresponding object with the raw email message in the S3 bucket. Based on the recipient address received in the event, email alias targets are located in the AWS SSM Parameter Store service.

### Environment variables

| Variable        | Description                                  |
| --------------- | -------------------------------------------- |
| EMAIL_BUCKET    | S3 bucket name with raw email objects        |
| ALIAS_MAP_PARAM | SSM parameter path with email alias mappings |

### Input data

The Lambda function is invoked by the AWS SES service.

#### SES event fragment:

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
```

#### SSM Parameter example

```json
{
  "alias1@foo.com": ["target1@bar.com"],
  "alias2@foo.com": ["target1@bar.com", "target2@bar.com"]
}
```

From the event, the messageId and destination, which contains the alias address, are extracted. The messageId is also the key name in the S3 bucket containing the email content.

- The Lambda function retrieves the email content from the S3 bucket.
- It adjusts the email to meet SES requirements.
- Acquires mail alias targets from the SSM Parameter Store
- It sends the modified email to the recipients of the email alias.
