import boto3
import datetime

def get_sqs_metrics(sqs_queue_url, session):
    # Get the queue ARN
    sqs_client = session.client('sqs')
    queue_attributes = sqs_client.get_queue_attributes(
        QueueUrl=sqs_queue_url,
        AttributeNames=['QueueArn']
    )
    queue_arn = queue_attributes['Attributes']['QueueArn']

    # Define the metric queries for the desired SQS metrics
    metric_queries = [
        {
            'Id': 'visible_messages',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/SQS',
                    'MetricName': 'ApproximateNumberOfMessagesVisible',
                    'Dimensions': [
                        {
                            'Name': 'QueueName',
                            'Value': queue_arn
                        }
                    ]
                },
                'Period': 60,
                'Stat': 'SampleCount'
            },
            'ReturnData': True
        },
        {
            'Id': 'not_visible_messages',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/SQS',
                    'MetricName': 'ApproximateNumberOfMessagesNotVisible',
                    'Dimensions': [
                        {
                            'Name': 'QueueName',
                            'Value': queue_arn
                        }
                    ]
                },
                'Period': 60,
                'Stat': 'SampleCount'
            },
            'ReturnData': True
        }
    ]

    # Define the time range for the metric data
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=1)

    # Get the metric data from CloudWatch
    cloudwatch_client = session.client('cloudwatch')
    metric_data = cloudwatch_client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=start_time,
        EndTime=end_time
    )

    return metric_data['MetricDataResults']

# Replace with the appropriate SQS queue URL and source account session
sqs_queue_url = 'https://sqs.<REGION>.amazonaws.com/<ACCOUNT_ID>/<QUEUE_NAME>'
source_account_session = ...  # Use the session created in the previous example

# Get the SQS metrics
sqs_metrics = get_sqs_metrics(sqs_queue_url, source_account_session)
print(sqs_metrics)
