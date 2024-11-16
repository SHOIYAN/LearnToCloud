from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Optional
import boto3

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("AWS_REGION"),  # Ensure AWS_REGION is set in your .env
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Get a reference to the DynamoDB table
table_name = "TvShowsTable"  # Update this to your actual table name in DynamoDB
table = dynamodb.Table(table_name)

@app.get("/")
async def root():
    return {"message": "Welcome to the TV Shows API!"}

@app.get("/api/shows")
async def get_tv_shows():
    try:
        # Scan to get all items; in production, consider optimizing or paginating if the table is large
        response = table.scan(
            ProjectionExpression="id, title"  # Only return id and title fields
        )
        items = response.get('Items', [])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing DynamoDB: {str(e)}")

@app.get("/api/seasons")
async def get_seasons(show_id: Optional[str] = Query(None, title="Show ID")):
    if not show_id:
        raise HTTPException(status_code=400, detail="Please provide a show_id query parameter. If unaware of the showId, check out the /api/shows endpoint.")

    try:
        # Query DynamoDB to find seasons based on show_id
        response = table.get_item(
            Key={'id': show_id},
            ProjectionExpression="seasons"
        )

        item = response.get('Item')
        if not item:
            return {"message": "No seasons found for the given show ID"}
        
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying DynamoDB: {str(e)}")

#remember to add ......
# AWS_REGION=your-aws-region
# AWS_ACCESS_KEY_ID=your-access-key-id
# AWS_SECRET_ACCESS_KEY=your-secret-access-key
