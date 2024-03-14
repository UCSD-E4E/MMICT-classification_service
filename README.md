# Docker Info

## Building our Docker image: 
Run this in the CLI: "docker build -t mmi-classification-websockets ."

Make sure you are in the same directory as the Dockerfile, in this case the root directory of our classification service repo.

## Running the Docker Container (For Devs):
Run this in the CLI: "docker run -p 5001:5001 mmi-classification-websockets"

We are mapping the localhost port to 5001, so to check if its working use http://localhost:5001 and open this in a browser.

## Image Details
We are building from a base image with ubuntu as our OS and a cuda runtime. As this is a Python service and we are ultilizing
Poetry for dependency management, the file structure follows the conventions of a Python package. The main script to run the server
is in the path "mm_classification/server.py". Running the server is defined in our Dockerfile entrypoint, so in order to run our
classification service as a container, just use the above "docker run" command in your CLI or in Docker Desktop.




