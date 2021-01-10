# bookstore-api


Connect the cloud machine
```shell
ssh root@134.209.96.49 
```

Create a DB in the cloud machine
```
docker run --name=bookstore-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=bookstore -p 5432:5432 -d postgres:10
```

Check the currently running processes 
```shell
docker ps
```

Stop one or more running container
```shell
docker stop container_name1 container_name2 ...
```

Remove one or more running container
```shell
docker rm container_name1 container_name2 ...
```


Connect the cloud machine via port 5432 for DB connection
```shell
ssh -L 5432:localhost:5432 -N -f -l root 134.209.96.49
```

Check out the “list of open files” on port 5432
```shell
lsof -i tcp:5432
```

Run FastAPI app locally
```shell
uvicorn run:app --reload --port 3000
```

## Redis

Run the following commands in the terminal of your cloud machine

Start a redis instance
```shell
docker run --name my-redis -d redis
```

```shell
docker run --name my-redis -d -p 6379:6379 redis
```
