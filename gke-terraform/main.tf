provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

variable "gcp_project_id" {}
variable "gcp_region" {}
variable "gke_cluster_name" {}
variable "gke_location" {}
variable "gke_node_pool_name" {}
variable "gke_machine_type" {}
variable "gke_min_nodes" { default = 0 }
variable "gke_max_nodes" { default = 3 }
variable "gke_disk_size" { default = 20 }

resource "google_container_cluster" "primary" {
  name     = var.gke_cluster_name
  location = var.gke_location  # Utilisation d'une variable pour la région
  
  remove_default_node_pool = true
  initial_node_count       = 1

  networking_mode = "VPC_NATIVE"
}

resource "google_container_node_pool" "primary_nodes" {
  name       = var.gke_node_pool_name
  location   = var.gke_location  # Variable pour la région
  cluster    = google_container_cluster.primary.name

  autoscaling {
    min_node_count = var.gke_min_nodes   
    max_node_count = var.gke_max_nodes   
  }

  node_config {
    machine_type = var.gke_machine_type
    disk_size_gb = var.gke_disk_size  
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
