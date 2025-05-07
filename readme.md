# GraphQL API with FastAPI, Strawberry, and S3 Parquet Integration

This project demonstrates how to build a GraphQL API using Python with FastAPI and Strawberry. The API can read data from Parquet files stored in AWS S3, perform aggregations using Pandas, and serve the results. It uses AWS IAM Identity Center (SSO) for AWS authentication.

## Features

*   GraphQL API endpoint.
*   Reads Parquet files from AWS S3.
*   Performs server-side data aggregations (e.g., sum by group) using Pandas.
*   Uses AWS IAM Identity Center (SSO) for secure AWS access.
*   Interactive GraphQL IDE (Apollo Sandbox) for testing.

## Setup Instructions

### 1. Prerequisites

*   Python 3.8+
*   AWS CLI v2 configured for IAM Identity Center (SSO) access.

### 2. Create and Activate a Python Virtual Environment

1st, `cd graphql_api`

**On macOS/Linux:**
```
python3 -m venv venv
source venv/bin/activate
or
python3 -m venv venv
```

**On Windows:**

```
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

**Explanation of dependencies:**
*   `fastapi`: The web framework used to build the API.
*   `strawberry-graphql[fastapi]`: The GraphQL library, with FastAPI integration.
*   `boto3`: The AWS SDK for Python, used to interact with S3.
*   `pandas`: Used for data manipulation, especially for reading Parquet files and performing aggregations.
*   `pyarrow`: Required by Pandas to read and write Parquet files.
*   `uvicorn[standard]`: An ASGI server to run the FastAPI application. `[standard]` includes helpful extras.
*   `python-dotenv`: To load environment variables from a `.env` file (optional, but good practice for configuration).
*   


### 5. Configure AWS Credentials (IAM Identity Center / SSO)

This application is set up to use an AWS SSO profile for authenticating with AWS services.
+   Create a .aws directory in the /graphql_api directory
+   Copy your aws profile (with access to our data lake) to config in /.aws
+   Create a .env file in the /graphql_api directory
+   list the following in your .env file:
    ```
        AWS_PROFILE=<profile in config>
        AWS_REGION=<your region>
    ```
