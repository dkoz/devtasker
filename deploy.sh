#!/bin/bash
set -e

DOCKER_IMAGE="dev-tasker"
CONTAINER_NAME="dev-tasker"
PORT="9050"

echo "Pulling the latest code from Git..."
git pull origin main

echo "Building the Docker image..."
docker build -t $DOCKER_IMAGE .

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping the existing container..."
    docker stop $CONTAINER_NAME
fi

if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
    echo "Removing the existing container..."
    docker rm $CONTAINER_NAME
fi

echo "Running the new container..."
docker run -d -p $PORT:$PORT -v $(pwd)/instance:/app/instance --name $CONTAINER_NAME $DOCKER_IMAGE

echo "Dev Tasker deployment complete."