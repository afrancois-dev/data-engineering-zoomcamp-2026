
# Docker
## Question 1
```
docker run -it --entrypoint=bash python:3.13-slim
uv pip -V
```
answer : 25.3

## Question 2
```
docker-compose up
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --user=postgres \
    --password=postgres \
    --host=db \
    --port=5433 \
    --db=ny_taxi
```
answer: db=5432 (as pgadmin is inside docker-compose network, it should use the internal port)

## Question 3

```
select count(*) from green_trips
where lpep_pickup_datetime >= '2025-11-01' and lpep_pickup_datetime < '2025-12-01'
and trip_distance <= 1
```
answer: 8007

## Question 4

```
select lpep_pickup_datetime::date, max(trip_distance) as max_distance 
from green_trips
where trip_distance < 100
group by lpep_pickup_datetime::date
order by max_distance DESC
```
answer: 2025-11-14 (if we refer to the single longest individual trip)

## Question 5

```
SELECT
    count(*) as total_amount,
    zpu."Zone" AS "pickup_loc"
FROM
    green_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
where t.lpep_pickup_datetime::date = '2025-11-18'
group by pickup_loc
order by total_amount desc
limit 1
```
answer: East Harlem North

## Question 6
```
SELECT
    tip_amount,
    zdo."Zone" AS "dropoff_loc"
FROM
    green_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
INNER JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
where t.lpep_pickup_datetime >= '2025-11-01' and t.lpep_pickup_datetime < '2025-12-01'
and zpu."Zone" = 'East Harlem North'
order by tip_amount desc
limit 1
```
answer: Yorkville West

# Terraform

## Question 7
answer: terraform init, terraform apply -auto-approve, terraform destroy

```
cd terraform/
terraform init 
terraform apply -auto-approve -var="project=endless-office-485017-f8"
```

Result
```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "EU"
      + max_time_travel_hours      = (known after apply)
      + project                    = "endless-office-485017-f8"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EU"
      + name                        = "terraform-demo-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 1
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning (known after apply)

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.
google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 2s [id=projects/endless-office-485017-f8/datasets/demo_dataset]
```
FYI : I use my local env, and I have already setup gcloud; therefore I don't have to specify the service account location
