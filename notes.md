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

