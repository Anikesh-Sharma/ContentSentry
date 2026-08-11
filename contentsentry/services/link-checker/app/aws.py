import boto3
from .config import settings

def _client(service: str):
    return boto3.client(
        service,
        region_name=settings.aws_region,
        endpoint_url=settings.aws_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

s3 = _client("s3")
sqs = _client("sqs")
dynamodb = _client("dynamodb")

def receive_job():
    """Long-poll SQS for one job. Returns the message dict or None."""
    resp = sqs.receive_message(
        QueueUrl=settings.jobs_queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=settings.poll_wait_seconds,
    )
    messages = resp.get("Messages", [])
    return messages[0] if messages else None

def delete_job(receipt_handle: str):
    """Delete a message from SQS after successful processing."""
    sqs.delete_message(
        QueueUrl=settings.jobs_queue_url,
        ReceiptHandle=receipt_handle,
    )

def download_content(bucket: str, key: str) -> str:
    """Fetch the raw content from S3 as a string."""
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj["Body"].read().decode("utf-8", errors="ignore")

def write_result(run_id: str, check_type: str, result: dict):
    """Write a check result to DynamoDB."""
    dynamodb.put_item(
        TableName=settings.results_table,
        Item={
            "run_id": {"S": run_id},
            "check_type": {"S": check_type},
            "total_links": {"N": str(result["total_links"])},
            "broken_links": {"N": str(result["broken_links"])},
            "details": {"S": result["details"]},
        },
    )
