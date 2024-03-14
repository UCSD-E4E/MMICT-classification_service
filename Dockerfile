# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Included this because installing GDAL would prompt the CLI to pick a geographic region
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies, ubuntu base image installs Python 3.10
# TODO: Look into using Conda for installing GDAL
RUN apt-get update && \
    apt-get install -y python3-pip libgdal-dev gdal-bin

# Verify GDAL version, rasterio needs GDAL to be >= version 3.1
RUN if [ $(gdal-config --version | cut -d '.' -f1,2) \< "3.1" ]; then echo "GDAL version installed is " $(gdal-config --version) && exit 1; fi

# Symlink between python3 and python
# This is a current workaround as running our server using my poetry entrypoint calls "python" instead of 3.10 which comes with our ubuntu image.
# Issue link: https://github.com/python-poetry/poetry/issues/6841 
RUN ln -s /bin/python3 /bin/python

# Install Poetry
RUN python3.10 -m pip install poetry

# Set working directory
WORKDIR /app

# Copy all application files, poetry lock file should be present in the same directory as our pyproject.toml file?
COPY . /app

# Install Python dependencies using poetry, poetry also generates an executable to run our server
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expose port
EXPOSE 5001

# Run our Flask app using poetry entrypoint
ENTRYPOINT ["/usr/local/bin/classification-server"]

