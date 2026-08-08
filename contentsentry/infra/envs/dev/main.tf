module "storage" {
  source      = "../../modules/storage"
  environment = var.environment
  project     = var.project
}

module "messaging" {
  source      = "../../modules/messaging"
  environment = var.environment
  project     = var.project
}

module "database" {
  source      = "../../modules/database"
  environment = var.environment
  project     = var.project
}
