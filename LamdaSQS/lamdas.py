import boto3
import json

def collect_sqs_metrics(accounts, regions):
    metrics = []
    for account_id in accounts:
        for region in regions:
            # Assume the cross-account role
            sts_client = boto3.client('sts')
            assumed_role = sts_client.assume_role(
                RoleArn=f'arn:aws:iam::{account_id}:role/CrossAccountSQSMetricsRole',
                RoleSessionName='sqs_metrics_collector'
            )

            # Create a session with the assumed role
            session = boto3.Session(
                aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                aws_session_token=assumed_role['Credentials']['SessionToken'],
                region_name=region
            )

            # Collect SQS metrics
            sqs_client = session.client('sqs')
            for queue_url in sqs_client.list_queues().get('QueueUrls', []):
                queue_name = queue_url.split('/')[-1]
                queue_attributes = sqs_client.get_queue_attributes(
                    QueueUrl=queue_url,
                    AttributeNames=['All']
                )['Attributes']
                metrics.append({
                    'account_id': account_id,
                    'region': region,
                    'queue_name': queue_name,
                    'queue_attributes': queue_attributes
                })

    return metrics

def lambda_handler(event, context):
    # List of account IDs and regions
    accounts = ['ACCOUNT_ID_1', 'ACCOUNT_ID_2']
    regions = ['us-east-1', 'us-west-2']

    # Collect metrics
    metrics = collect_sqs_metrics(accounts, regions)

    # Save metrics to S3
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket='YOUR_S3_BUCKET_NAME',
        Key='sqs_metrics.json',
        Body=json.dumps(metrics)
    )

    return {
        'statusCode': 200,
        'body': json.dumps('SQS metrics collected successfully.')
    }
