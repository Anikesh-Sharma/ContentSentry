import boto3
from .config import settings

def _client(service: str):
    """Create a boto3 client pointed at LocalStack (or real AWS)."""
    return boto3.client(
        service,
        region_name=settings.aws_region,
        endpoint_url=settings.aws_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

s3 = _client("s3")
sqs = _client("sqs")

def upload_content(key: str, body: bytes, content_type: str = "text/html"):
    """Store raw content in the S3 bucket."""
    s3.put_object(
        Bucket=settings.raw_content_bucket,
        Key=key,
        Body=body,
        ContentType=content_type,
    )

def enqueue_job(message_body: str):
    """Push a job onto the SQS jobs queue."""
    sqs.send_message(
        QueueUrl=settings.jobs_queue_url,
        MessageBody=message_body,
    )