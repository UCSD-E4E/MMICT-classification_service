# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND noninteractive


# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3-pip libpq-dev libgdal-dev gdal-bin

# Verify GDAL version
RUN if [ $(gdal-config --version | cut -d '.' -f1,2) \< "3.1" ]; then echo $(gdal-config --version) && exit 1; fi

# Install Poetry
RUN pip3 install poetry

# Set working directory
WORKDIR /app

# Copy only pyproject.toml and poetry.lock (if exists) to cache dependencies
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app

# Expose port
EXPOSE 5001

# Start the application
CMD ["python3", "server.py"]
