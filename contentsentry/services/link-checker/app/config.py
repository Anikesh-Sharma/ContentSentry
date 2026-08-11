from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AWS / LocalStack connection
    aws_region: str = "us-east-1"
    aws_endpoint_url: str = "http://localhost:4566"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"

    # Resources
    jobs_queue_url: str = "http://localhost:4566/000000000000/contentsentry-jobs-dev"
    results_table: str = "contentsentry-results-dev"

    # Worker behaviour
    poll_wait_seconds: int = 20   # long-polling: wait up to 20s for a message
    link_timeout: float = 5.0     # seconds to wait per link check

    class Config:
        env_file = ".env"

settings = Settings()
