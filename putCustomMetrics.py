"""
This script defines a function put_sqs_metric_data that takes a dictionary containing SQS metric data and publishes it as CloudWatch custom metrics. The script then iterates through the sqs_metrics list and calls the function for each dictionary. You can add the rest of the metrics in the same format as QueueSize and NumberOfMessagesSent.

Keep in mind that CloudWatch might charge you for custom metrics, so be cautious when publishing a large number of metrics. For more information on CloudWatch pricing, refer to the official AWS documentation.

https://aws.amazon.com/cloudwatch/pricing/
"""


import boto3

sqs_metrics = [
    {
        'queuename': 'queue1',
        'region': 'us-west-2',
        'org': 'organization1',
        'account': '123456789012',
        'queueSize': 35,
        'numberOfMessagesSent': 120,
        'numberOfMessagesReceived': 115,
        'numberOfMessagesDeleted': 110,
        'approximateAgeOfOldestMessage': 42,
        'sentMessageSize': 512
    },
    {
        'queuename': 'queue2',
        'region': 'us-east-1',
        'org': 'organization2',
        'account': '210987654321',
        'queueSize': 10,
        'numberOfMessagesSent': 50,
        'numberOfMessagesReceived': 45,
        'numberOfMessagesDeleted': 40,
        'approximateAgeOfOldestMessage': 30,
        'sentMessageSize': 1024
    }
]

def put_sqs_metric_data(metric_data):
    cloudwatch = boto3.client('cloudwatch', region_name=metric_data['region'])

    cloudwatch.put_metric_data(
        Namespace='SQSMetrics',
        MetricData=[
            {
                'MetricName': 'QueueSize',
                'Dimensions': [
                    {'Name': 'QueueName', 'Value': metric_data['queuename']},
                    {'Name': 'Org', 'Value': metric_data['org']},
                    {'Name': 'Account', 'Value': metric_data['account']}
                ],
                'Value': metric_data['queueSize'],
                'Unit': 'Count'
            },
            {
                'MetricName': 'NumberOfMessagesSent',
                'Dimensions': [
                    {'Name': 'QueueName', 'Value': metric_data['queuename']},
                    {'Name': 'Org', 'Value': metric_data['org']},
                    {'Name': 'Account', 'Value': metric_data['account']}
                ],
                'Value': metric_data['numberOfMessagesSent'],
                'Unit': 'Count'
            },
            # ... Add the rest of the metrics here in the same format
        ]
    )

for metric_data in sqs_metrics:
    put_sqs_metric_data(metric_data)
