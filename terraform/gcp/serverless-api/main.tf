terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  type    = string
  default = "patterns-fixture-project"
}

provider "google" {
  project = var.project_id
  region  = "us-central1"
}

resource "google_cloud_run_service" "api_endpoint" {
  name     = "serverless-api-endpoint"
  location = "us-central1"
  project  = var.project_id

  template {
    spec {
      containers {
        image = "gcr.io/cloudrun/hello"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloudfunctions_function" "handler" {
  name                  = "serverless-api-handler"
  project               = var.project_id
  region                = "us-central1"
  runtime               = "python311"
  entry_point           = "handler"
  trigger_http          = true
  source_archive_bucket = "patterns-fixture-source"
  source_archive_object = "serverless-api-handler.zip"
}

resource "google_firestore_database" "items" {
  name        = "serverless-api-items"
  project     = var.project_id
  location_id = "us-central1"
  type        = "FIRESTORE_NATIVE"
}
