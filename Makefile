.PHONY: help build up down logs shell clean test

# Default target
help:
	@echo "AetherAI Docker Management"
	@echo "=========================="
	@echo ""
	@echo "Available commands:"
	@echo "  make build       - Build Docker image"
	@echo "  make up          - Start containers in detached mode"
	@echo "  make down        - Stop and remove containers"
	@echo "  make logs        - View container logs"
	@echo "  make shell       - Open shell in running container"
	@echo "  make clean       - Remove containers, volumes, and images"
	@echo "  make test        - Test Docker image"
	@echo "  make rebuild     - Clean and rebuild everything"
	@echo "  make push        - Push image to registry"
	@echo ""

# Build Docker image
build:
	@echo "Building AetherAI Docker image..."
	docker-compose build --no-cache

# Start containers
up:
	@echo "Starting AetherAI containers..."
	docker-compose up -d
	@echo "Containers started! Use 'make logs' to view output"

# Stop containers
down:
	@echo "Stopping AetherAI containers..."
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Open shell in container
shell:
	docker exec -it aetherai_terminal /bin/bash

# Run the application interactively
run:
	docker exec -it aetherai_terminal python terminal/main.py

# Clean up everything
clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v --rmi all
	@echo "Cleanup complete!"

# Test the image
test:
	@echo "Testing AetherAI Docker image..."
	docker-compose run --rm aetherai python -c "import sys; print(f'Python {sys.version}'); sys.exit(0)"
	@echo "Test passed!"

# Rebuild everything from scratch
rebuild: clean build up

# Push to registry (requires login)
push:
	@echo "Pushing image to GitHub Container Registry..."
	docker tag aetherai:latest ghcr.io/kunjshah95/aetherai:latest
	docker push ghcr.io/kunjshah95/aetherai:latest

# Pull from registry
pull:
	@echo "Pulling latest image from registry..."
	docker pull ghcr.io/kunjshah95/aetherai:latest
