resource "aws_sqs_queue" "jobs_dlq" {
  name                      = "${var.project}-jobs-dlq-${var.environment}"
  message_retention_seconds = 1209600
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_sqs_queue" "jobs" {
  name                       = "${var.project}-jobs-${var.environment}"
  visibility_timeout_seconds = var.visibility_timeout
  message_retention_seconds  = 86400
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.jobs_dlq.arn
    maxReceiveCount     = 3
  })
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}
