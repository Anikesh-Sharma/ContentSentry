resource "aws_dynamodb_table" "results" {
  name         = "${var.project}-results-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "run_id"
  range_key    = "check_type"

  attribute {
    name = "run_id"
    type = "S"
  }
  attribute {
    name = "check_type"
    type = "S"
  }
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_dynamodb_table" "runs" {
  name         = "${var.project}-runs-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "run_id"

  attribute {
    name = "run_id"
    type = "S"
  }
  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}
