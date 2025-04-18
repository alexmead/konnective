
### FastAPI Run locally
To run the FastAPI app locally for development run the following command:
```shell
uvicorn main:app --reload
```

## Docker
### Build Docker
To build the docker container, first ensure you have Docker Desktop installed and running. Then, run the following command from the ws-konnektive-wrapper/api directory:
```shell
docker build -t fastapi-app .
```
## Run Docker Container Locally
Further, to run the container you just built to test locally, run the following command:
```shell
docker run -d -p 8000:8000 --name fastapi-container fastapi-app
```


Further commands to build the container image, tage the image, then push it to AWS ECR. 
Note, you will need to "cross-build" for the proper runtime architecture...

# The x86 Deployment:
####################

docker buildx build --platform linux/amd64 -t fastapi-app-86 . 

# Will likely not work on a local machine due to architecture differences:
docker run -d -p 8000:8000 --name fastapi-container-86 fastapi-app-86

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 189187172192.dkr.ecr.us-east-2.amazonaws.com

# The ECR Repo only needs to be created one time:
aws ecr create-repository --repository-name fastapi-app-86 --image-scanning-configuration scanOnPush=true --region us-east-2

docker tag fastapi-app-86:latest 189187172192.dkr.ecr.us-east-2.amazonaws.com/fastapi-app-86:latest

docker push 189187172192.dkr.ecr.us-east-2.amazonaws.com/fastapi-app-86:latest

