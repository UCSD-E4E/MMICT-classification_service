building our Docker image: 

docker build -t mmi-classification-websockets .

running the Docker container (For Devs):

docker run -p 5001:5001 mmi-classification-websockets  

We are mapping the localhost port to 5001, so to check if its working use http://localhost:5001 
