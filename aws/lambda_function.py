# This function is deployed and executed in AWS Lambda.
# It is triggered by AWS IoT Core rules when telemetry messages arrive.
# This file is kept here for reference and version control purposes.
import json
import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TelemetryReadings')

def lambda_handler(event, context):
    try:
        print(f"Received event: {json.dumps(event)}")
        
        # IoT Core sends the message directly as the event
        table.put_item(Item={
            'deviceId': event['deviceId'],
            'timestamp': event['timestamp'],
            'temperature': Decimal(str(event['temperature'])),
            'pressure': Decimal(str(event['pressure'])),
            'vibration': Decimal(str(event['vibration'])),
            'receivedAt': datetime.utcnow().isoformat()
        })
        
        print(f"Stored reading for {event['deviceId']}")
        
        return {
            'statusCode': 200,
            'body': 'Record stored successfully'
        }
        
    except Exception as e:
        print(f"Error: {e}")
        raise e