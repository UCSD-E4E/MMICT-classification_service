# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
    libgl1-mesa-glx\
    gdal-bin \
    libgdal-dev
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy files to working directory
COPY . .

# Expose port
EXPOSE 8000

# Start the application
# CMD ["python3", "server.py"]
CMD ["python3", "-m", "gunicorn", "-w", "4", "server:app"]