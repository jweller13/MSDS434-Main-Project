from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery

app = FastAPI()

client = bigquery.Client()


class Complaint(BaseModel):
    product: str | None = None
    subproduct: str | None = None
    issue: str | None = None
    subissue: str | None = None
    company_name: str | None = None
    state: str | None = None
    submitted_via: str | None = None
    consumer_consent_provided: str | None = None
    consumer_tags: str | None = None
    has_narrative: int | None = None
    narrative_character_count: int | None = None
    narrative_word_count: int | None = None
    month_received: int | None = None
    days_to_send_to_company: int | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(complaint: Complaint):

    query = """
    SELECT *
    FROM ML.PREDICT(
      MODEL `msds-434-502817.cfpb_data.monetary_relief_model`,
      (
        SELECT
          @product AS product,
          @subproduct AS subproduct,
          @issue AS issue,
          @subissue AS subissue,
          @company_name AS company_name,
          @state AS state,
          @submitted_via AS submitted_via,
          @consumer_consent_provided AS consumer_consent_provided,
          @consumer_tags AS consumer_tags,
          @has_narrative AS has_narrative,
          @narrative_character_count AS narrative_character_count,
          @narrative_word_count AS narrative_word_count,
          @month_received AS month_received,
          @days_to_send_to_company AS days_to_send_to_company
      )
    )
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("product", "STRING", complaint.product),
            bigquery.ScalarQueryParameter("subproduct", "STRING", complaint.subproduct),
            bigquery.ScalarQueryParameter("issue", "STRING", complaint.issue),
            bigquery.ScalarQueryParameter("subissue", "STRING", complaint.subissue),
            bigquery.ScalarQueryParameter("company_name", "STRING", complaint.company_name),
            bigquery.ScalarQueryParameter("state", "STRING", complaint.state),
            bigquery.ScalarQueryParameter("submitted_via", "STRING", complaint.submitted_via),
            bigquery.ScalarQueryParameter(
                "consumer_consent_provided",
                "STRING",
                complaint.consumer_consent_provided
            ),
            bigquery.ScalarQueryParameter(
                "consumer_tags",
                "STRING",
                complaint.consumer_tags
            ),
            bigquery.ScalarQueryParameter(
                "has_narrative",
                "INT64",
                complaint.has_narrative
            ),
            bigquery.ScalarQueryParameter(
                "narrative_character_count",
                "INT64",
                complaint.narrative_character_count
            ),
            bigquery.ScalarQueryParameter(
                "narrative_word_count",
                "INT64",
                complaint.narrative_word_count
            ),
            bigquery.ScalarQueryParameter(
                "month_received",
                "INT64",
                complaint.month_received
            ),
            bigquery.ScalarQueryParameter(
                "days_to_send_to_company",
                "INT64",
                complaint.days_to_send_to_company
            ),
        ]
    )

    rows = list(client.query(query, job_config=job_config).result())
    result = dict(rows[0])

    probability = next(
        item["prob"]
        for item in result["predicted_monetary_relief_probs"]
        if item["label"] == 1
    )

    threshold = 0.75
    prediction = probability >= threshold

    return {
        "predicted_monetary_relief": prediction,
        "probability": round(probability, 4),
        "threshold": threshold
    }