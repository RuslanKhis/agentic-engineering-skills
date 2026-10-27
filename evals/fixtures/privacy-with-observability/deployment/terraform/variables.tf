variable "project_id" { type = string }
variable "project_name" {
  type    = string
  default = "travel-desk-agent"
}
variable "region" {
  type    = string
  default = "europe-west1"
}
variable "container_image" { type = string }

resource "google_service_account" "app_sa" {
  account_id = "${var.project_name}-app"
  project    = var.project_id
}
