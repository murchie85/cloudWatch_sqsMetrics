"""


This script creates and updates a custom CloudWatch metric. 
To access the metric later via an API call, you can use the get_metric_data or get_metric_statistics 
methods provided by the CloudWatch client in Boto3.
"""

import boto3

# Create a CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='us-west-2')

# Define the custom metric
namespace = 'MyCustomNamespace'
metric_name = 'MyCustomMetric'

# Publish the custom metric
cloudwatch.put_metric_data(
    Namespace=namespace,
    MetricData=[
        {
            'MetricName': metric_name,
            'Dimensions': [
                {
                    'Name': 'MyDimension',
                    'Value': 'MyDimensionValue'
                },
            ],
            'Value': 100,  # This is the initial value of the metric
            'Unit': 'Count'
        },
    ]
)

# Update the custom metric later
cloudwatch.put_metric_data(
    Namespace=namespace,
    MetricData=[
        {
            'MetricName': metric_name,
            'Dimensions': [
                {
                    'Name': 'MyDimension',
                    'Value': 'MyDimensionValue'
                },
            ],
            'Value': 200,  # This is the updated value of the metric
            'Unit': 'Count'
        },
    ]
)
