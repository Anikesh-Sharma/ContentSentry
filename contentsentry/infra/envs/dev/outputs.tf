output "raw_content_bucket" {
  value = module.storage.raw_content_bucket_name
}

output "reports_bucket" {
  value = module.storage.reports_bucket_name
}

output "jobs_queue_url" {
  value = module.messaging.jobs_queue_url
}

output "jobs_dlq_url" {
  value = module.messaging.jobs_dlq_url
}

output "results_table" {
  value = module.database.results_table_name
}

output "runs_table" {
  value = module.database.runs_table_name
}
