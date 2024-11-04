import os
import json
import boto3
from botocore.exceptions import ClientError


# Initialize the S3 resource
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")

# Specify your bucket name
bucket_name = "album-coverz-buck3t"  # Replace with your desired bucket name

# Create the S3 bucket
try:
    bucket = s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully.")
except ClientError as e:
    print(f"Error creating bucket: {e}")

# Disable Block Public Access settings for the bucket
try:
    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )
    print(f"Successfully disabled Block Public Access for bucket '{bucket_name}'.")
except Exception as e:
    print(f"Error disabling Block Public Access: {e}")


# Define the bucket policy
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::album-coverz-buck3t/*"],
            "Condition": {
                "StringEquals": {
                    "s3:ExistingObjectTag/content-type": "image/jpeg",
                    "s3:ExistingObjectTag/content-type": "image/png"
                }
            }
        }
    ]
}


# Convert the policy to JSON
bucket_policy_json = json.dumps(bucket_policy)

# Set the bucket policy
try:
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
    print("Bucket policy set to allow public read access.")
except Exception as e:
    print(f"Error setting bucket policy: {e}")


#Function to upload all files in a local folder to S3

# Function to upload all files in a local folder to S3 with specific headers
def upload_folder_to_s3(local_folder, s3_folder):
    for root, _, files in os.walk(local_folder):
        for file_name in files:
            local_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(local_path, local_folder)
            s3_key = f"{s3_folder}/{relative_path}"
            
            # Determine content type based on file extension
            content_type = "image/jpeg" if file_name.lower().endswith(".jpg") or file_name.lower().endswith(".jpeg") else "image/png"
            
            # Upload with specific content type
            bucket.upload_file(
                Filename=local_path,
                Key=s3_key,
                ExtraArgs={
                    "ContentType": content_type,  # Set content type to display inline
                    "ContentDisposition": "inline"  # Suggest inline display
                }
            )
            print(f"Uploaded {local_path} to {s3_key} in bucket '{bucket_name}' with Content-Type: {content_type}")

# Example usage: specify your local folder and S3 folder
local_folder_path = "./assets/"  # Local path to the folder
s3_folder_path = "my-album_coverz"  # Desired folder path in the S3 bucket
upload_folder_to_s3(local_folder_path, s3_folder_path)


# List all objects in the bucket
response = s3_client.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    for obj in response['Contents']:
        object_key = obj['Key']
        # Set the ACL to public-read
        s3_client.put_object_acl(Bucket=bucket_name, Key=object_key, ACL='public-read')
        print(f"ACL for '{object_key}' set to public-read.")
else:
    print("No objects found in the bucket.")



#/////////////////////////////////////////////////////////////////////DynamoDB////////////////////////////////////////////////////////////////////////

# Initializing my DynamoDB resource
db = boto3.resource("dynamodb")
table_name = "musicdb"



# Create the DynamoDB table
try:
    table = db.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'album_id',  # Primary key
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'album_id',
                'AttributeType': 'S'  # S for String
            }
        ],
        BillingMode='PAY_PER_REQUEST'  # Use on-demand capacity
    )
    print(f"Creating table '{table_name}'...")
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table '{table_name}' created successfully.")
except ClientError as e:
    print(f"Error creating table: {e.response['Error']['Message']}")



# List of music data to add
music_data = [
    {
        "album_id": "ANTI",
        "title": "ANTI",
        "artist": "Rihanna",
        "releaseYear": "2016",
        "genre": "R&B",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/ANTI+album+cover.jpg"
    },
    {
        "album_id": "Beauty Behind the Madness",
        "title": "Beauty Behind the Madness",
        "artist": "The Weeknd",
        "releaseYear": "2015",
        "genre": "R&B, Pop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/Beauty+Behind+the+Madness+album+cover.jpg"
    },
    {
        "album_id": "Birds in the Trap Sing McKnight",
        "title": "Birds in the Trap Sing McKnight",
        "artist": "Travis Scott",
        "releaseYear": "2016",
        "genre": "Hip Hop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/Birds+in+the+Trap+Sing+McKnight+album+cover.jpg"
    },
    {
        "album_id": "Views",
        "title": "Views",
        "artist": "Drake",
        "releaseYear": "2016",
        "genre": "Hip Hop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/drave+cover+views.jpg"
    },
    {
        "album_id": "DS2",
        "title": "DS2",
        "artist": "Future",
        "releaseYear": "2015",
        "genre": "Hip Hop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/DS2+album+cover.jpg"
    },
    {
        "album_id": "If You’re Reading This It’s Too Late",
        "title": "If You’re Reading This It’s Too Late",
        "artist": "Drake",
        "releaseYear": "2015",
        "genre": "Hip Hop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/If+You%E2%80%99re+Reading+This+It%E2%80%99s+Too+Late+album+cover.jpg"
    },
    {
        "album_id": "Rodeo",
        "title": "Rodeo",
        "artist": "Travis Scott",
        "releaseYear": "2015",
        "genre": "Hip Hop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/Rodeo+album+cover.jpg"
    },
    {
        "album_id": "Starboy",
        "title": "Starboy",
        "artist": "The Weeknd",
        "releaseYear": "2016",
        "genre": "R&B, Pop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/starboy_album_cover.jpg"
    },
    {
        "album_id": "The Pinkprint",
        "title": "The Pinkprint",
        "artist": "Nicki Minaj",
        "releaseYear": "2014",
        "genre": "Hip Hop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/The+Pinkprint+album+cover.jpg"
    },
    {
        "album_id": "What a Time to Be Alive",
        "title": "What a Time to Be Alive",
        "artist": "Future & Drake",
        "releaseYear": "2015",
        "genre": "Hip Hop",
        "coverUrl": "https://album-coverz-buck3t.s3.us-east-1.amazonaws.com/my-album_coverz/What+a+Time+to+Be+Alive+album+cover.jpg"
    }
]


# Add items to the DynamoDB table
for data in music_data:
    try:
        table.put_item(Item=data)  # Using 'data' variable
        print(f"Added {data['title']} by {data['artist']} to the table.")
    except ClientError as e:
        print(f"Error adding item: {e.response['Error']['Message']}")


#/////////////////////////////////////////////////////////////////////Lambda////////////////////////////////////////////////////////////////////////

# Create the GetAlbums Lambda Function

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('musicdb')

def lambda_handler(event, context):
    try:
        # Scan the DynamoDB table to get all albums
        response = table.scan()
        albums = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps(albums)
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


#Create the GetAlbumsByYear Lambda Function

def lambda_handler(event, context):
    year = event['pathParameters']['year']  # Extract the year from the request
    try:
        # Query the DynamoDB table to get albums for the specified year
        response = table.scan(
            FilterExpression='releaseYear = :year',
            ExpressionAttributeValues={
                ':year': year
            }
        )
        albums = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps(albums)
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
