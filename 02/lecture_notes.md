# Kestra

## 2.1.1
- already know orchestrator concept

## 2.1.2
- NoCode or Code (AI to help coding pipelines)
- kestra pipelines can run on every languages (Python, Go, ...)
- more than 1000 of connectors
- RAG

## 2.2.1
```
mkdir 02/
docker compose up -d
```

## 2.2.2
- flows (having an id that cannot be changed)
  - tasks (having also an id that can be updated)
   - .Return task -> output
  - inputs
    - at the start of the execution I can fill a variable
  - variables
    - can use inputs into a variable
    - e.g can be used to chain inputs -> url
      - need to be render() in order to display inputs inside
  - PluginDefaults
    - e.g log level : ERROR | INFO ...
  - triggers
   - when the pipelines starts
   - disabled : to run it manually
  - concurrency
   - how many execution can run in //

- UI Exploration (Logs, Gantt, Execution...)

## 2.2.3
- python orchestration
  - https://www.youtube.com/watch?v=VAHm0R_XjqI

## 2.3.1 
- first taxi pipeline on kestra !
  - extract, transform and query tasks
    - underneath output -> preview Tasks -> 2 files (data.json (we started from here) and product.json)

## 2.3.2
- https://www.youtube.com/watch?v=Z9ZmmwtXDcU

## 2.3.3
- https://www.youtube.com/watch?v=1pu_C_oOAMA
 - scheduling : backfill thanks to the UI, and check whether data is here through pgadmin (local db)
