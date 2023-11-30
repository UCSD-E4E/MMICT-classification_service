build image:

docker build -t mmi-classification-websockets .

run:

docker run mmi-classification-websockets
OR
docker run -e AWS_ACCESS_KEY_ID=[access key here] -e AWS_SECRET_ACCESS_KEY=[access key here] mmi-classification-websockets

might need to pip install flask-sock but added to requirements.txt
