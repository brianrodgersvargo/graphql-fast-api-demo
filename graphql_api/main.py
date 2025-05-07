import io
import os
import pandas as pd
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from dotenv import load_dotenv
# from services.config_loader import load_config
import boto3


load_dotenv()
# load_config()
aws_profile = os.getenv('AWS_PROFILE')
aws_region = os.getenv('AWS_REGION')
debits_bucket_name = 'ds-dev-reporting-framework'
debits_file_key = "data/ecgps_payments_dashboard/transforms/issuance_balance/debits/part-00000-760525d8-288e-44c9-a673-3855bef5c800-c000.snappy.parquet"
# session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

@strawberry.type
class Debit:
    sponsor_id: str
    sponsor_name: str
    client_id: str
    display_name: str
    study_id: str
    study_name: str
    parent_site_number: str
    parent_legal_name: str
    iso_code: str
    country: str
    total_debits: float

@strawberry.type
class SponsorDebitSummary:
    sponsorName: str
    sumOfDebits: float

@strawberry.type
class Query:
    @strawberry.field
    async def debits_from_s3(self) -> list[Debit]:

        # Create a Boto3 session for s3
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        s3_client = session.client('s3')
        
        # Get the Parquet file object from S3
        s3_object = s3_client.get_object(
            Bucket=debits_bucket_name,
            Key=debits_file_key
        )
        
        # Read parquet bytes into pandas df
        parquet_bytes = s3_object['Body'].read()
        df = pd.read_parquet(io.BytesIO(parquet_bytes))
        
        # extract list of debits
        debits_list = []
        for index, row in df.iterrows():
            debits_list.append(
                Debit(
                    sponsor_id=row['sponsor_id'],
                    sponsor_name=row['sponsor_name'],
                    client_id=row['client_id'],
                    display_name=row['display_name'],
                    study_id=row['study_id'],
                    study_name=row['study_name'],
                    parent_site_number=row['parent_site_number'],
                    parent_legal_name=row['parent_legal_name'],
                    iso_code=row['iso_code'],
                    country=row['country'],
                    total_debits=row['total_debits']
                )
            )
        return debits_list
    @strawberry.field
    async def debitSummaryBySponsor(self) -> list[SponsorDebitSummary]:
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        s3_client = session.client('s3')
        
        # Get the Parquet file object from S3
        s3_object = s3_client.get_object(
            Bucket=debits_bucket_name,
            Key=debits_file_key
        )
        
        # Read parquet bytes into pandas df
        parquet_bytes = s3_object['Body'].read()
        df = pd.read_parquet(io.BytesIO(parquet_bytes))


        # Group by 'sponsorName' and sum 'totalDebits'
        aggregated_debits_df = df.groupby('sponsor_name')['total_debits'].sum().reset_index()

        # Convert the aggregated DataFrame rows to SponsorDebitSummary objects
        summary_list = []
        for index, row in aggregated_debits_df.iterrows():
            summary_list.append(
                SponsorDebitSummary(
                    sponsorName=row['sponsor_name'],
                    sumOfDebits=row['total_debits'] # This is the sum for the group
                )
            )
        
        return summary_list
            

schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema, graphql_ide="apollo-sandbox")
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Hello! Your GraphQL API is at /graphql"}
