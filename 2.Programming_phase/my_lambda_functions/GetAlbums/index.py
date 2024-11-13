import json
import boto3
from botocore.exceptions import ClientError

# Initialize a DynamoDB resource
db = boto3.resource("dynamodb")
table = db.Table("musicdb")  # Replace with your actual DynamoDB table name

def lambda_handler(event, context):
    try:
        # Scan the DynamoDB table to get all items (albums)
        response = table.scan()
        albums = response.get('Items', [])

        # Return a successful response
        return {
            'statusCode': 200,
            'body': json.dumps(albums)
        }
    except ClientError as e:
        # Handle error response
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
