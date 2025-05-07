import os
import boto3
from dotenv import load_dotenv

# Load the environment variables from the .env file 
load_dotenv()


def load_local_secrets():
    """
    Load secrets from AWS Secrets Manager and parameters from SSM Parameter Store in local development
    and set them as environment variables.
    """
    aws_profile = os.getenv('AWS_PROFILE')
    aws_region = os.getenv('AWS_REGION')

    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

    # secrets_manager = session.client("secretsmanager")
    # ssm = session.client("ssm")

    # secret_qlik_idp = secrets_manager.get_secret_value(SecretId='/ds/dev/qlik-idp')['SecretString']
    # secret_qlik_idp_dict = eval(secret_qlik_idp) 
    
    # os.environ['QLIK_ISSUER'] = secret_qlik_idp_dict['issuer'] 
    # os.environ['QLIK_KEY_ID'] = secret_qlik_idp_dict['key_id']  
    # os.environ['QLIK_PRIVATE_KEY'] = secret_qlik_idp_dict['private']

    # secret_qlik_client = secrets_manager.get_secret_value(SecretId='/ds/dev/qlik-client')['SecretString']
    # secret_qlik_client_dict = eval(secret_qlik_client)  
    # os.environ['QLIK_CLIENT_ID'] = secret_qlik_client_dict['qilk_internal_client_id']  
    # os.environ['QLIK_CLIENT_SECRET'] = secret_qlik_client_dict['qlik_internal_client_secret']  
    # os.environ['QLIK_HOST'] = secret_qlik_client_dict['qlik_host'] 
    # os.environ['QLIK_INTEGRATION_ID'] = secret_qlik_client_dict['qlik_integration_id']  
    
    # os.environ['QLIK_SERVICE_TOKEN'] = secrets_manager.get_secret_value(SecretId='/ds/sandbox/qlik-service-api-token')['SecretString']

    # ping_client_id = ssm.get_parameter(Name='/ds/dev/internal-ping-client-id', WithDecryption=True)['Parameter']['Value']
    # os.environ['PINGONE_CLIENT_ID'] = ping_client_id  

    # ping_env_id = ssm.get_parameter(Name='/ds/dev/ping-env-id', WithDecryption=True)['Parameter']['Value']
    # os.environ['PINGONE_ENV_ID'] = ping_env_id  

    # os.environ['PINGONE_AUTH_URI'] = "https://auth.pingone.com"  

    print("Local secrets and parameters loaded into environment variables.")


def check_kubernetes_env():
    """
    Check if the necessary environment variables are set in Kubernetes.
    """
    # required_env_vars = [
    #     'QLIK_ISSUER', 'QLIK_KEY_ID', 'QLIK_PRIVATE_KEY',
    #     'QLIK_CLIENT_ID', 'QLIK_CLIENT_SECRET', 'QLIK_HOST', 'QLIK_INTEGRATION_ID',
    #     'PINGONE_CLIENT_ID', 'PINGONE_ENV_ID', 'PINGONE_AUTH_URI',
    #     'QLIK_SERVICE_TOKEN'
    # ]

    required_env_vars = []

    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables for Kubernetes: {', '.join(missing_vars)}")
    else:
        print("All required environment variables are set for Kubernetes.")
    
    print('testing ping env id')
    print(os.getenv('PINGONE_ENV_ID'))

def load_config():
    print('testing env')
    print(os.getenv("ENVIRONMENT"))
    """
    Load configuration based on the environment (local or Kubernetes).
    """
    if os.getenv("ENVIRONMENT", "local") == "Kubernetes":
        return check_kubernetes_env()
    else:
        return load_local_secrets()