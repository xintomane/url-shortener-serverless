import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortUrls')

def lambda_handler(event, context):
    code = event["pathParameters"]["code"]

    response = table.get_item(Key={"shortCode": code})
    item = response.get("Item")
    if not item:
        return {"statusCode": 404, "body": "Not found"}

    # Increment clicks atomically
    table.update_item(
        Key={"shortCode": code},
        UpdateExpression="SET clicks = if_not_exists(clicks, :zero) + :one",
        ExpressionAttributeValues={":one": 1, ":zero": 0},
    )

    return {
        "statusCode": 302,
        "headers": {"Location": item["longUrl"]}
    }