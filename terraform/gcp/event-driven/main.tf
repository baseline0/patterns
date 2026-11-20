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

resource "google_pubsub_topic" "events" {
  name    = "events"
  project = var.project_id
}

resource "google_pubsub_topic" "events_dead_letter" {
  name    = "events-dead-letter"
  project = var.project_id
}

resource "google_pubsub_subscription" "events" {
  name                 = "events-consumer"
  project              = var.project_id
  topic                = google_pubsub_topic.events.name
  ack_deadline_seconds = 20

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.events_dead_letter.id
    max_delivery_attempts = 5
  }
}

resource "google_cloudfunctions_function" "consumer" {
  name                  = "event-driven-consumer"
  project               = var.project_id
  region                = "us-central1"
  runtime               = "python311"
  entry_point           = "consume"
  source_archive_bucket = "patterns-fixture-source"
  source_archive_object = "event-driven-consumer.zip"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.events.id
  }
}

resource "google_firestore_database" "processed_events" {
  name        = "processed-events"
  project     = var.project_id
  location_id = "us-central1"
  type        = "FIRESTORE_NATIVE"
}
