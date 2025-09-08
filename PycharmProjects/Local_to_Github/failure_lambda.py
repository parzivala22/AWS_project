import json
import boto3
import os

# Create SNS client
sns = boto3.client("sns")

# Correct way: get value from environment variable
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")


def lambda_handler(event, context):
    """
    Lambda function to send Step Function failure details to SNS.
    """
    try:
        # Extract error details from event
        error_info = json.dumps(event, indent=2)

        # Message for SNS
        message = (
            "🚨 Step Function Pipeline Failed!\n\n"
            f"Error Details:\n{error_info}"
        )

        # Publish message to SNS
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Step Function Pipeline Failure Alert"
        )

        print("SNS Publish Response:", response)

        return {
            "statusCode": 200,
            "body": "Failure notification sent successfully"
        }

    except Exception as e:
        print("Error sending SNS notification:", str(e))
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }