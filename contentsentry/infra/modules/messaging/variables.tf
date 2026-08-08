variable "environment" {
  type = string
}
variable "project" {
  type    = string
  default = "contentsentry"
}
variable "visibility_timeout" {
  type    = number
  default = 300
}
