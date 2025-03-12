provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

variable "gcp_project_id" {}
variable "gcp_region" {}

variable "composer_env_name" {}
variable "composer_image_version" {
  default = "composer-2-airflow-2"
}

resource "google_composer_environment" "composer_env" {
  name   = var.composer_env_name
  region = var.gcp_region

  config {
    software_config {
      image_version = var.composer_image_version
    }

    workloads_config {
      scheduler {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 5
        count      = 1
      }

      web_server {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 5
      }

      worker {
        cpu        = 2
        memory_gb  = 4
        storage_gb = 2
        min_count  = 1
        max_count  = 3
      }
    }
  }
}
