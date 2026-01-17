# Docker

execute containers
```
docker run -it ubuntu
apt update
apt install python3
python3 -V
docker run -it python:3.13.11-slim
docker run -it --entrypoint=bash python:3.13.11-slim
```

list docker containers
```
docker ps -a
```

remove all docker containers
```
docker rm `docker ps -aq`
```

# UV - env
```
pip install uv
uv venv
source .venv/bin/activate
uv add ...
```

# Docker inside pipeline dir

build container with image:tag
```
docker build -t test:pandas .
```

run container
```
docker run test:pandas 1
```

debug container and then don't save state (e.g files created, etc...)
```
docker run -it --entrypoint=bash test:pandas --rm
```
:warning: The speaker creates a venv inside the container. On my mind it is not necessary to add a venv inside a docker container as the env is already isolated with docker :warning:


# Postgres inside docker
mkdir ny_taxi_postgres_data

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# Data ingestion

:info: we could use a modern notebook like marimo  :info:

# Creating data ingestion script

```
uv run jupyter nbconvert --to=script notebook.ipynb
```

run converted jupyter notebook
```
uv run python ingest_data.py   --user=root   --password=root   --host=localhost   --port=5432   --db=ny_taxi   --table=yellow_taxi_trips
```

# pgAdmin
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```

create virtual docker network 

```
docker network create pg-network
```

then we must run both containers on the same network
```
# Run PostgreSQL on the network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# In another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```