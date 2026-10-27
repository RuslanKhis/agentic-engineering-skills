variable "project_id" {
  type        = string
  description = "Project that hosts the agent."
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "project_name" {
  type    = string
  default = "claims-helper"
}
