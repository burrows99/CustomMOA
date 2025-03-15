#!/bin/bash

# Define container and image names
CONTAINER_NAME="custom_moa"
IMAGE_NAME="custom-moa"

# Function to stop and remove the container if it exists
cleanup_container() {
    if docker ps -a --filter name=^/$CONTAINER_NAME$ --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
        echo "Stopping and removing existing container: $CONTAINER_NAME"
        docker stop "$CONTAINER_NAME" && docker rm "$CONTAINER_NAME"
    fi
}

# Clean up any existing container
cleanup_container

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

# Run the Docker container
echo "Running Docker container: $CONTAINER_NAME"
docker run -d -p 8000:8000 --name "$CONTAINER_NAME" "$IMAGE_NAME"