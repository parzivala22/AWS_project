import json
import boto3
import os

sf_client = boto3.client("stepfunctions")

def lambda_handler(event, context):
     # Extract bucket and key from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']


    print(f"Triggered by file: s3://{bucket}/{key}")

    # Start Step Function Execution
    response = sf_client.start_execution(
        stateMachineArn="arn:aws:states:ap-south-1:960631463855:stateMachine:pk_step_function",
        input=json.dumps({
            "bucket": bucket,
            "key": key
        })
    )

    return {
        "statusCode": 200,
        "body": json.dumps(f"Started Step Function {response['executionArn']} for {key}")
    }