resource "google_bigquery_dataset" "telemetry" {
  dataset_id = "${replace(var.project_name, "-", "_")}_telemetry"
  project    = var.project_id
  location   = var.region
}

resource "google_logging_project_sink" "genai_details" {
  name                   = "${var.project_name}-genai-details"
  project                = var.project_id
  destination            = "bigquery.googleapis.com/projects/${var.project_id}/datasets/${google_bigquery_dataset.telemetry.dataset_id}"
  filter                 = "labels.\"event.name\"=\"gen_ai.client.inference.operation.details\""
  unique_writer_identity = true
}

resource "google_bigquery_table" "completions" {
  dataset_id = google_bigquery_dataset.telemetry.dataset_id
  table_id   = "completions"
  project    = var.project_id
  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = ["gs://${google_storage_bucket.logs_data_bucket.name}/completions/*"]
  }
}
