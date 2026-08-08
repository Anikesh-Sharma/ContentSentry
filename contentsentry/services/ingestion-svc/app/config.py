from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AWS / LocalStack
    aws_region: str = "us-east-1"
    aws_endpoint_url: str = "http://localhost:4566"  # LocalStack
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"

    # Resources (from our Terraform outputs)
    raw_content_bucket: str = "contentsentry-raw-content-dev"
    jobs_queue_url: str = (
        "http://localhost:4566/000000000000/contentsentry-jobs-dev"
    )

    class Config:
        env_file = ".env"

settings = Settings()