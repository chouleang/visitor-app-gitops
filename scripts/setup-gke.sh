#!/bin/bash

# Variables
PROJECT_ID="it-enviroment"
CLUSTER_NAME="gitops-cluster"
REGION="us-central1"
ZONE="us-central1-a"

# Set project
gcloud config set project $PROJECT_ID

# Create GKE cluster with Workload Identity enabled
gcloud container clusters create $CLUSTER_NAME \
    --region $REGION \
    --num-nodes=1 \
    --machine-type=e2-medium \
    --disk-size=50\
    --disk-type=pd-standard\
    --enable-ip-alias \
    --workload-pool=$PROJECT_ID.svc.id.goog \
    --release-channel=regular
# Get credentials
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION

# Create namespace for application
kubectl create namespace visitor-app
kubectl create namespace argocd

echo "GKE cluster setup complete!"
