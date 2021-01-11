# Bookstore API

Follow through the Udemy course _Complete Backend (API) Development with Python AZ_

## Tech Stack

- Python 3.8
- Docker + uvicorn
- FastAPI
- PostgreSQL
- Redis
  
## Virtual Dedicated Server
- Digital Ocean


## Connect via SSH to the server

```shell
ssh root@[server IP address]
```

## Install Docker on Ubuntu

https://docs.docker.com/engine/install/ubuntu/


## PostgreSQL Database Creation and Connection

Create a DB in the server
```
docker run --name=bookstore-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=bookstore -p 5432:5432 -d postgres:10
```

Check the currently running processes 
```shell
docker ps
```

Stop one or more running container
```shell
docker stop container1 [container2...]
```

Remove one or more running container
```shell
docker rm container1 [container2...]
```

Create the bridge on port 5432 from the server to the local host 
```shell
ssh -L 5432:localhost:5432 -N -f -l root [server IP address]
```

Check out the “list of open files” on port 5432
```shell
lsof -i tcp:5432
```

Kill processes on port 5432
```shell
kill `lsof -ti tcp:5432`
```

## FastAPI

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

Start a redis instance on port 6379
```shell
docker run --name my-redis -d -p 6379:6379 redis
```


```shell
ssh -L 6379:localhost:6379 -N -f -l root [server IP address]
```

## Testing

Create and run a Test DB locally
```shell
docker run --name=test-db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5432:5432 -d postgres:10
```

Create and run a redis test instance locally
```shell
docker run --name=test-redis -d -p 6379:6379 redis
```

Execute queries in `bookstore.sql` to create table schemas

Then run tests
```shell
python -m unittest tests/all_test.py
```

### Load Testing

#### Locust

```shell
locust -f ./tests/locust_load_test.py
```

#### ApacheBench

Install ApacheBench. Then under the /tests folder, run:

```shell
ab -n 100 -c 5 -H "Authorization : Bearer {jwt}" -p ab_jsons/post_user.json http://127.0.0.1:3000/v1/user
ab -n 1000 -c 10 -H "Authorization : Bearer {jwt}" http://127.0.0.1:3000/v1/book/isbn2
```

## Deployment

Change the server's IP address in deploy.sh and run:
```shell
/bin/bash ./deploy.sh
```

Check the logs
```shell
docker logs -f bookstore-api
```