# Clean Dockerfile for AetherAI (inspect before replacing terminal/Dockerfile)
# Use a small official Python image
FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Install common system dependencies required to build wheels and multimedia
# Keep the list minimal to reduce image size. Add packages as specific failures appear.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    pkg-config \
    libssl-dev \
    libpq-dev \
    libsndfile1 \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
# Ensure pip, setuptools and wheel are up-to-date to prefer wheels over sdists
RUN python -m pip install --upgrade pip setuptools wheel
# Allow build backends to access project files during isolated builds if necessary
ENV PIP_NO_BUILD_ISOLATION=0
RUN sh -c "pip install --no-cache-dir -r /app/requirements.txt || ( echo 'WARNING: pip install failed — see errors above. Inspect failing package logs.'; exit 1 )"

# Copy application source
COPY . /app

# Create and switch to a non-root user for runtime
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} appuser && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash appuser
USER appuser

# Default command – adjust if your entrypoint differs
CMD ["python", "main.py"]
