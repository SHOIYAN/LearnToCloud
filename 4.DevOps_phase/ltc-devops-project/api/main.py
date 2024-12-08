from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import boto3
from typing import Optional

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
table_name = "musicdb"
table = dynamodb.Table(table_name)

@app.get("/")
async def root():
    return {"message": "Welcome to the Music Albums API!"}

@app.get("/getalbums")
async def get_albums():
    try:
        # Scan to get all items
        response = table.scan(
            ProjectionExpression="album_id, title, artist, genre, releaseYear, coverUrl"  # Fields to return
        )
        items = response.get('Items', [])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing DynamoDB: {str(e)}")

@app.get("/albumsbyyear/{year}")
async def get_albums_by_year(year: int = Path(..., title="Release Year")):
    try:
        # Query DynamoDB to find albums based on the release year
        response = table.scan(
            FilterExpression="releaseYear = :year",
            ExpressionAttributeValues={":year": str(year)},
            ProjectionExpression="title, artist, genre, releaseYear, coverUrl"
        )
        items = response.get('Items', [])
        if not items:
            return {"message": "No albums found for the given year"}
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying DynamoDB: {str(e)}")
