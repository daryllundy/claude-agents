provider "google" {
  project = "my-project"
  region  = "us-central1"
}

resource "google_storage_bucket" "data" {
  name     = "my-gcp-bucket"
  location = "US"
}
