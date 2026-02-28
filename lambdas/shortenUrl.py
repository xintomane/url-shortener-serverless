import json
import string
import random
import boto3
from datetime import datetime, timezone, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortUrls')

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def lambda_handler(event, context):
    body_raw = event.get("body")
    body = json.loads(body_raw) if isinstance(body_raw, str) else (body_raw or event)

    long_url = body.get("url")
    if not long_url:
        return {"statusCode": 400, "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Missing url"})}

    # TTL: expire after 90 days (change as you like)
    ttl_seconds = int((datetime.now(timezone.utc) + timedelta(days=90)).timestamp())

    code = generate_code()
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    table.put_item(
        Item={
            "shortCode": code,
            "longUrl": long_url,
            "createdAt": now_iso,
            "clicks": 0,
            "ttl": ttl_seconds
        }
    )

    return {"statusCode": 200, "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"shortCode": code})}