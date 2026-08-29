# MSDS434-Main-Project
# CFPB Monetary Relief Prediction API

This project is a cloud-native machine learning application built for MSDS 434. It uses Consumer Financial Protection Bureau (CFPB) consumer complaint data to predict whether a complaint is likely to result in monetary relief.

The application combines a BigQuery ML logistic regression model with a FastAPI service deployed to Google Cloud Run. The project is connected to GitHub through Cloud Build so that changes pushed to the `main` branch automatically trigger a new deployment.

## Project Overview

The goal of this project is to demonstrate an end-to-end cloud analytics workflow that includes:

- Public data ingestion and analysis
- Feature engineering
- Machine learning model development in BigQuery ML
- Model evaluation and threshold selection
- API development with FastAPI
- Containerization with Docker
- Deployment to Google Cloud Run
- Automated deployment from GitHub using Cloud Build

The model predicts whether a CFPB consumer complaint will result in monetary relief.

## Architecture

The project follows this general workflow:

```text
CFPB Consumer Complaint Data
        ↓
BigQuery
        ↓
BigQuery ML Logistic Regression Model
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

Any change pushed to the GitHub main branch automatically triggers Cloud Build, which rebuilds the Docker container and deploys a new revision of the application to Cloud Run.

Repository Structure
MSDS434-Main-Project/
├── Dockerfile
├── .gitignore
├── app/
│   ├── main.py
│   └── requirements.txt
└── Videos/
Dockerfile

Defines the Python container used to run the FastAPI application.

app/main.py

Contains the FastAPI application and prediction endpoint.

app/requirements.txt

Contains the Python dependencies required by the application.

Technologies Used
Google Cloud Platform
BigQuery
BigQuery ML
Cloud Run
Cloud Build
Docker
Python
FastAPI
Uvicorn
Pydantic
GitHub
Machine Learning Model

The application uses a BigQuery ML logistic regression model named:

msds-434-502817.cfpb_data.monetary_relief_model

The model predicts whether a complaint is likely to result in monetary relief.

The prediction API uses a classification threshold of:

0.75

A predicted probability greater than or equal to 0.75 is classified as a positive prediction for monetary relief.

Model Features

The API accepts the following complaint characteristics:

Product
Subproduct
Issue
Subissue
Company name
State
Submission method
Consumer consent status
Consumer tags
Narrative availability
Narrative character count
Narrative word count
Month received
Days to send to company
API Endpoints
Health Check
GET /health

Example response:

{
  "status": "ok"
}

This endpoint confirms that the FastAPI service is running.

Prediction
POST /predict

The endpoint accepts complaint information in JSON format and sends those values to the BigQuery ML model.

Example request:

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

Example response:

{
  "predicted_monetary_relief": true,
  "probability": 0.9768,
  "threshold": 0.75
}
Testing the API

The deployed application can be tested from Google Cloud Shell using curl.

Example:

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
Automated Deployment

The application is configured for continuous deployment from GitHub.

When changes are pushed to the main branch:

git add .
git commit -m "Describe changes"
git push

the following process occurs automatically:

GitHub
   ↓
Cloud Build Trigger
   ↓
Docker Build
   ↓
Cloud Run Deployment

This allows the deployed application to stay synchronized with the source code stored in GitHub.

Docker Configuration

The project uses a Python 3.11 container.

The Dockerfile:

Creates a Python environment
Installs required dependencies
Copies the FastAPI application into the container
Starts the application using Uvicorn on port 8080

Cloud Run automatically routes traffic to the application through port 8080.

Security

The application does not store Google Cloud credentials inside the GitHub repository.

Authentication with BigQuery is handled through the Google Cloud service account associated with the deployed Cloud Run service.

Sensitive files such as environment files, credentials, and Python cache files are excluded from source control through .gitignore.

Project Purpose

This project demonstrates how cloud-native services can be combined to create a scalable machine learning application.

The application moves from raw consumer complaint data to a deployed prediction API while incorporating automated software deployment practices.

Author

Jazz Weller

Northwestern University
Master of Science in Data Science
MSDS 434
