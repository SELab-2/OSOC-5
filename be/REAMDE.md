# OSOC-5: Back-end

## Usage
Starting the Docker container:
```
cd docker
docker-compose up -d --build
```

This will start the back-end and the database container.

Stopping the containers is easily done with `docker-compose down`.

### Note on ARM

If you have an ARM processor, (for now) you need to build the docker for amd64, due to an [issue](https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentifcation-problem) with the dependencies for postgresql 14.

```
docker-compose down
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose up -d --build
```


