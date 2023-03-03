# Base image
FROM nvidia/cuda:11.4.2-cudnn8-runtime-ubuntu20.04

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1-mesa-glx

# Copy files to working directory
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 8000

# Start the application
CMD ["python3", "server.py"]