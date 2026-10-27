resource "google_cloud_run_v2_service" "app" {
  name     = var.project_name
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    service_account = google_service_account.app_sa.email
    containers {
      image = var.container_image

      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name  = "LOGS_BUCKET_NAME"
        value = google_storage_bucket.logs_data_bucket.name
      }
      env {
        name  = "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"
        value = "NO_CONTENT"
      }
      env {
        name  = "ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS"
        value = "false"
      }
      env {
        name  = "ANALYTICS_DATASET"
        value = google_bigquery_dataset.analytics.dataset_id
      }
    }
  }
}

resource "google_storage_bucket" "logs_data_bucket" {
  name                        = "${var.project_id}-${var.project_name}-logs"
  location                    = var.region
  project                     = var.project_id
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = "travel_desk_analytics"
  project    = var.project_id
  location   = var.region
}
