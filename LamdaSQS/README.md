1. Enable AWS Organizations if you haven't already. This allows you to centrally manage your multiple accounts and apply policies across them.

2. Create an AWS Lambda function that retrieves SQS queue metrics using the AWS SDK for Python (Boto3). This function will be triggered periodically to fetch metrics from all the queues.

3. Configure cross-account access by creating a role in each account that allows the Lambda function to access the SQS queues. Attach a policy that grants the necessary permissions to read the SQS metrics.

4. Create an Amazon S3 bucket to store the collected metrics. This bucket should be accessible by your Python application for further processing.

5. Set up VPC peering to enable communication between VPCs in different regions. This ensures that the Lambda function can access the SQS queues across regions.

6. Modify the Lambda function to store the retrieved metrics in the S3 bucket.