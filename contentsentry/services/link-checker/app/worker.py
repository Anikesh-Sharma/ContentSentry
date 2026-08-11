import json
import time

from .aws import receive_job, delete_job, download_content, write_result
from .checker import check_links

CHECK_TYPE = "link-checker"

def process_message(message: dict):
    body = json.loads(message["Body"])
    run_id = body["run_id"]
    bucket = body["s3_bucket"]
    key = body["s3_key"]

    print(f"[{CHECK_TYPE}] Processing run_id={run_id} key={key}")

    # 1. Download content from S3
    html = download_content(bucket, key)

    # 2. Run the link check
    result = check_links(html)
    print(
        f"[{CHECK_TYPE}] run_id={run_id} "
        f"total_links={result['total_links']} "
        f"broken={result['broken_links']}"
    )

    # 3. Write result to DynamoDB
    write_result(run_id, CHECK_TYPE, result)

    # 4. Delete the message from SQS (mark as done)
    delete_job(message["ReceiptHandle"])
    print(f"[{CHECK_TYPE}] Done run_id={run_id}\n")

def main():
    print(f"[{CHECK_TYPE}] Worker started. Polling for jobs...")
    while True:
        try:
            message = receive_job()
            if message is None:
                # no message this poll cycle; loop again
                continue
            process_message(message)
        except KeyboardInterrupt:
            print(f"\n[{CHECK_TYPE}] Shutting down.")
            break
        except Exception as e:
            print(f"[{CHECK_TYPE}] ERROR: {e}")
            time.sleep(2)  # brief pause before retrying

if __name__ == "__main__":
    main()
