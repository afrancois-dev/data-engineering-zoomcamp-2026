# Redpanda

## Beforehand
- set-up python (with uv)
 - `pip install uv`
 - `uv add kafka-python pandas pyarrow`
 - `uvx pgcli -h localhost -p 5432 -U postgres -d postgres`
- set-up docker
 - get the docker-compose.yml from github repo.
 - `docker compose up redpanda -d`
 - `docker compose logs redpanda -f`

- useful commands for redpanda
```
docker exec -it redpanda-redpanda-1 rpk topic delete rides && docker exec -it redpanda-redpanda-1 rpk topic create rides
```

We are going to 
    1. create a producer
    2. create a consumer

## Questions

1. Redpanda version
```
(redpanda) @afrancois-dev ➜ /workspaces/data-engineering-zoomcamp-2026/07/redpanda (main) $ docker exec -it redpanda-redpanda-1 rpk version
rpk version: v25.3.9
Git ref:     836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
Build date:  2026 Feb 26 07 48 21 Thu
OS/Arch:     linux/amd64
Go version:  go1.24.3

Redpanda Cluster
  node-1  v25.3.9 - 836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
```
answer: v25.3.9

2. Sending data to Redpanda
