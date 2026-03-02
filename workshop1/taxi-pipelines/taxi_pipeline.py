import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def taxi_pipeline_source():
    """Définition de la source dlt pour l'API NYC Taxi."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
            "paginator": {
                "type": "page_number",
                "base_page": 1,
                "total_path": None,
                "stop_after_empty_page": True,
            },
        },
        "resources": [
            {
                "name": "taxi_data",
                "endpoint": {
                    "path": "",
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_taxi_data():
    """Charge les données de l'API dans DuckDB."""
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data",
    )

    load_info = pipeline.run(taxi_pipeline_source())
    print(load_info)


if __name__ == "__main__":
    load_taxi_data()
