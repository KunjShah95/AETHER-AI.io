FROM python:3.11-slim

# Install system deps for optional features (git, curl, ffmpeg placeholder)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy only necessary files
COPY pyproject.toml .
COPY terminal/ terminal/
COPY README.md LICENSE ./

# Install minimal runtime dependencies
RUN pip install --no-cache-dir .

# Default to running the interactive CLI
ENTRYPOINT ["aetherai"]
