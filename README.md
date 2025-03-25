
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
