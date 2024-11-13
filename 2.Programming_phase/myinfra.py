import os
import json
import boto3
import botocore
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


# Initialize IAM and Lambda clients
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda') 

# Define the trust policy that allows Lambda to assume the role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"  # AWS Lambda service principal
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# Create the role with the trust policy
role_name = "LambdaDynamoDBReadOnlyRole"
try:
    role = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description="Role for Lambda functions to read from DynamoDB and access S3"
    )
    print(f"Created role with name: {role_name}")
except iam_client.exceptions.EntityAlreadyExistsException:
    print(f"Role {role_name} already exists.")
    role = iam_client.get_role(RoleName=role_name)

# Verify and update the trust policy if needed
iam_client.update_assume_role_policy(
    RoleName=role_name,
    PolicyDocument=json.dumps(trust_policy)
)

# Attach the DynamoDB read-only policy to the role
iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn="arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess"
)

# Attach the S3 full access policy to the role
iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
)

# Use the role ARN in your Lambda creation/update code
role_arn = role['Role']['Arn']

# Create the GetAlbums Lambda function
response_get_albums = lambda_client.create_function(
    FunctionName="GetAlbums",
    Runtime="python3.12",
    Role=role_arn,
    Handler="lambda_function.lambda_handler",
    Code={
        'S3Bucket': "album-coverz-buck3t",       # Replace with your S3 bucket name
        'S3Key': "my_lambda_zips/GetAlbums.zip"      # Make sure the path is correct
    },
    Description="Lambda function to retrieve albums from DynamoDB",
    Timeout=10,
    MemorySize=128
)
print("Created GetAlbums function.")

# Create the GetAlbumsByYear Lambda function
response_get_albums_by_year = lambda_client.create_function(
    FunctionName="GetAlbumsByYear",
    Runtime="python3.12",
    Role=role_arn,
    Handler="lambda_function.lambda_handler",
    Code={
        'S3Bucket': "album-coverz-buck3t",       # Replace with your S3 bucket name
        'S3Key': "my_lambda_zips/GetAlbumsByYear.zip"  # Ensure the path is correct
    },
    Description="Lambda function to retrieve albums by year from DynamoDB",
    Timeout=10,
    MemorySize=128
)
print("Created GetAlbumsByYear function.")



#////////////////////////////////////////////////API_GATEWAY////////////////////////////////////////////////////////////////////////////////////////


# Initialize Boto3 clients
apigateway = boto3.client('apigateway')
lambda_client = boto3.client('lambda')

# Define your existing Lambda function names
get_albums_lambda_name = "GetAlbums"
get_albums_by_year_lambda_name = "GetAlbumsByYear"
account_id = '...........'
region = 'us-east-1'

# Step 1: Create the API Gateway
try:
    api_response = apigateway.create_rest_api(
        name='AlbumAPI',
        description='API to retrieve albums from DynamoDB',
    )
    api_id = api_response['id']
    print(f"Created API with ID: {api_id}")
except botocore.exceptions.ClientError as e:
    print(f"Error creating API: {e}")

# Step 2: Get the root resource ID
try:
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = resources['items'][0]['id']
    print(f"Root resource ID: {root_id}")
except botocore.exceptions.ClientError as e:
    print(f"Error getting resources: {e}")

# Step 3: Create /getalbums resource
resource_path_albums = 'getalbums'
try:
    resource_response = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart=resource_path_albums
    )
    resource_id_albums = resource_response['id']
    print(f"Created resource /{resource_path_albums} with ID: {resource_id_albums}")
except botocore.exceptions.ClientError as e:
    print(f"Error creating resource /{resource_path_albums}: {e}")

# Step 4: Create GET method for /getalbums
try:
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id_albums,
        httpMethod='GET',
        authorizationType='NONE'
    )
    print(f"Created GET method for /{resource_path_albums}.")
except botocore.exceptions.ClientError as e:
    print(f"Error creating GET method for /{resource_path_albums}: {e}")

# Step 5: Integrate GET method with GetAlbums Lambda function
lambda_function_arn_get = f"arn:aws:lambda:{region}:{account_id}:function:{get_albums_lambda_name}"

try:
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id_albums,
        httpMethod='GET',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_function_arn_get}/invocations'
    )
    print(f"Linked GET method to {get_albums_lambda_name} Lambda function.")
except botocore.exceptions.ClientError as e:
    print(f"Error linking GET method to {get_albums_lambda_name}: {e}")

# Step 6: Add permission for API Gateway to invoke GetAlbums Lambda function
try:
    lambda_client.add_permission(
        FunctionName=get_albums_lambda_name,
        StatementId='ApiGatewayInvokeGetAlbums',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:{region}:{account_id}:{api_id}/*/GET/{resource_path_albums}'
    )
    print("Added permission for API Gateway to invoke GetAlbums Lambda function.")
except botocore.exceptions.ClientError as e:
    print(f"Error adding permission for GetAlbums: {e}")

# Step 7: Create /getalbumsbyyear resource
resource_path_by_year = 'getalbumsbyyear'
try:
    resource_response_by_year = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart=resource_path_by_year
    )
    resource_id_by_year = resource_response_by_year['id']
    print(f"Created resource /{resource_path_by_year} with ID: {resource_id_by_year}")
except botocore.exceptions.ClientError as e:
    print(f"Error creating resource /{resource_path_by_year}: {e}")

# Step 8: Create {year} as a child resource of /getalbumsbyyear
try:
    year_resource_response = apigateway.create_resource(
        restApiId=api_id,
        parentId=resource_id_by_year,
        pathPart='{year}'  # Define {year} as a path parameter
    )
    year_resource_id = year_resource_response['id']
    print(f"Created resource /{resource_path_by_year}/{{year}} with ID: {year_resource_id}")
except botocore.exceptions.ClientError as e:
    print(f"Error creating resource /{resource_path_by_year}/{{year}}: {e}")

# Step 9: Create GET method for /getalbumsbyyear/{year}
try:
    apigateway.put_method(
        restApiId=api_id,
        resourceId=year_resource_id,
        httpMethod='GET',
        authorizationType='NONE',
        requestParameters={
            'method.request.path.year': True  # Enable the year path parameter
        }
    )
    print(f"Created GET method for /{resource_path_by_year}/{{year}}.")
except botocore.exceptions.ClientError as e:
    print(f"Error creating GET method for /{resource_path_by_year}/{{year}}: {e}")

# Step 10: Integrate GET method with GetAlbumsByYear Lambda function
lambda_function_arn_by_year = f"arn:aws:lambda:{region}:{account_id}:function:{get_albums_by_year_lambda_name}"

try:
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=year_resource_id,
        httpMethod='GET',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_function_arn_by_year}/invocations',
        requestParameters={
            'integration.request.path.year': 'method.request.path.year'
        }
    )
    print(f"Linked GET method to {get_albums_by_year_lambda_name} Lambda function.")
except botocore.exceptions.ClientError as e:
    print(f"Error linking GET method to {get_albums_by_year_lambda_name}: {e}")

# Step 11: Add permission for API Gateway to invoke GetAlbumsByYear Lambda function
try:
    lambda_client.add_permission(
        FunctionName=get_albums_by_year_lambda_name,
        StatementId='ApiGatewayInvokeGetAlbumsByYear',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:{region}:{account_id}:{api_id}/*/GET/{resource_path_by_year}/*'
    )
    print("Added permission for API Gateway to invoke GetAlbumsByYear Lambda function.")
except botocore.exceptions.ClientError as e:
    print(f"Error adding permission for GetAlbumsByYear: {e}")

# Step 12: Deploy the API
try:
    deployment_response = apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    print("API deployed successfully.")
except botocore.exceptions.ClientError as e:
    print(f"Error deploying API: {e}")
