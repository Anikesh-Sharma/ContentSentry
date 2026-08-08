resource "aws_s3_bucket" "raw_content" {
  bucket = "${var.project}-raw-content-${var.environment}"
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_s3_bucket" "reports" {
  bucket = "${var.project}-reports-${var.environment}"
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}
