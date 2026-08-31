# CFPB Monetary Relief Prediction API

A cloud-native machine learning application developed for **Northwestern University MSDS 434**.

This project uses Consumer Financial Protection Bureau (CFPB) consumer complaint data to predict whether a complaint is likely to result in **monetary relief**.

The application combines a **BigQuery ML logistic regression model** with a **FastAPI** service deployed to **Google Cloud Run**. The project is connected to GitHub through **Cloud Build**, allowing changes pushed to the `main` branch to automatically trigger a new deployment.

---

## Project Overview

The goal of this project is to demonstrate an end-to-end cloud analytics and machine learning workflow, including:

- Public data ingestion and analysis
- Feature engineering
- Machine learning model development with BigQuery ML
- Model evaluation and classification threshold selection
- API development with FastAPI
- Containerization with Docker
- Deployment to Google Cloud Run
- Continuous deployment from GitHub using Cloud Build

The final application exposes a REST API that accepts consumer complaint characteristics and returns a prediction indicating whether the complaint is likely to result in monetary relief.

---

## Architecture

The project follows this general workflow:

```text
CFPB Consumer Complaint Data
            ↓
         BigQuery
            ↓
BigQuery ML Logistic Regression
            ↓
     FastAPI Application
            ↓
     Docker Container
            ↓
    Google Cloud Run
            ↑
       Cloud Build
            ↑
          GitHub
```

Changes pushed to the GitHub `main` branch automatically trigger Cloud Build, which rebuilds the Docker container and deploys a new revision of the application to Cloud Run.

---

## Repository Structure

```text
MSDS434-Main-Project/
├── Dockerfile
├── .gitignore
├── app/
│   ├── main.py
│   └── requirements.txt
└── Videos/
```

### `Dockerfile`

Defines the Python container used to run the FastAPI application.

### `app/main.py`

Contains the FastAPI application, health check, input schema, BigQuery integration, and prediction endpoint.

### `app/requirements.txt`

Contains the Python dependencies required by the application.

### `.gitignore`

Prevents unnecessary or sensitive local files from being committed to the repository.

---

## Technologies Used

- **Google Cloud Platform**
  - BigQuery
  - BigQuery ML
  - Cloud Run
  - Cloud Build
- **Python**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **Docker**
- **GitHub**

---

## Machine Learning Model

The application uses a BigQuery ML logistic regression model:

```text
msds-434-502817.cfpb_data.monetary_relief_model
```

The model predicts whether a CFPB consumer complaint is likely to result in monetary relief.

### Classification Threshold

The prediction API uses a classification threshold of:

```text
0.75
```

A predicted probability greater than or equal to **0.75** is classified as a positive prediction for monetary relief.

---

## Model Features

The API accepts the following complaint characteristics:

- Product
- Subproduct
- Issue
- Subissue
- Company name
- State
- Submission method
- Consumer consent status
- Consumer tags
- Narrative availability
- Narrative character count
- Narrative word count
- Month received
- Days to send complaint to company

---

## API Endpoints

### Health Check

**Endpoint**

```text
GET /health
```

**Example response**

```json
{
  "status": "ok"
}
```

This endpoint confirms that the FastAPI service is running successfully.

---

### Prediction

**Endpoint**

```text
POST /predict
```

The endpoint accepts complaint information in JSON format and sends the provided feature values to the BigQuery ML model.

**Example request**

```json
{
  "product": "Checking or savings account",
  "subproduct": "Checking account",
  "issue": "Managing an account",
  "subissue": "Fee problem",
  "company_name": "BANK OF AMERICA, NATIONAL ASSOCIATION",
  "state": "VA",
  "submitted_via": "Web",
  "consumer_consent_provided": "Consent provided",
  "consumer_tags": null,
  "has_narrative": 1,
  "narrative_character_count": 500,
  "narrative_word_count": 90,
  "month_received": 8,
  "days_to_send_to_company": 2
}
```

**Example response**

```json
{
  "predicted_monetary_relief": true,
  "probability": 0.9768,
  "threshold": 0.75
}
```

---

## Testing the API

The deployed application can be tested using `curl` from Google Cloud Shell or another terminal that supports curl.

### Cloud Run URL

```text
https://msds434-main-project-546200181633.us-east4.run.app
```

### Example Prediction Request

```bash
curl -X POST https://msds434-main-project-546200181633.us-east4.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product": "Checking or savings account",
    "subproduct": "Checking account",
    "issue": "Managing an account",
    "subissue": "Fee problem",
    "company_name": "BANK OF AMERICA, NATIONAL ASSOCIATION",
    "state": "VA",
    "submitted_via": "Web",
    "consumer_consent_provided": "Consent provided",
    "consumer_tags": null,
    "has_narrative": 1,
    "narrative_character_count": 500,
    "narrative_word_count": 90,
    "month_received": 8,
    "days_to_send_to_company": 2
  }'
```
**Example request needs to be formatted like this**

```json
curl -X POST https://msds434-main-project-546200181633.us-east4.run.app/predict -H "Content-Type: application/json" -d "{\"product\":\"Checking or savings account\",\"subproduct\":\"Checking account\",\"issue\":\"Managing an account\",\"subissue\":\"Fee problem\",\"company_name\":\"BANK OF AMERICA, NATIONAL ASSOCIATION\",\"state\":\"VA\",\"submitted_via\":\"Web\",\"consumer_consent_provided\":\"Consent provided\",\"consumer_tags\":null,\"has_narrative\":1,\"narrative_character_count\":500,\"narrative_word_count\":90,\"month_received\":8,\"days_to_send_to_company\":2}"
```
---

## Automated Deployment

The application is configured for continuous deployment from GitHub.

When changes are committed and pushed to the `main` branch:

```bash
git add .
git commit -m "Describe changes"
git push
```

the following deployment process occurs automatically:

```text
GitHub
   ↓
Cloud Build Trigger
   ↓
Docker Image Build
   ↓
Cloud Run Deployment
```

This allows the deployed application to remain synchronized with the source code stored in GitHub.

---

## Docker Configuration

The project uses a **Python 3.11** container.

The Dockerfile:

1. Creates the Python application environment
2. Installs the required dependencies
3. Copies the FastAPI application into the container
4. Starts the application using Uvicorn
5. Exposes the application through port `8080`

Google Cloud Run automatically routes incoming traffic to the application through port `8080`.

---

## Security

Google Cloud credentials are **not stored in the GitHub repository**.

Authentication with BigQuery is handled through the Google Cloud service account associated with the deployed Cloud Run service.

Sensitive or unnecessary local files, including credentials, environment files, and Python cache files, are excluded from source control through `.gitignore`.

---

## Project Purpose

This project demonstrates how cloud-native data and application services can be combined to create a scalable machine learning application.

The solution moves from raw CFPB consumer complaint data through feature engineering and machine learning model development to a deployed prediction API. It also incorporates containerization and continuous deployment practices to demonstrate an end-to-end cloud software development workflow.

---

## Author

**Jazz Weller**

Northwestern University  
Master of Science in Data Science  
MSDS 434
