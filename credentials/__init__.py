import boto3

def initialize_aws_session():
    """Initialize AWS session with credentials for local development."""
    boto3.setup_default_session(
        aws_access_key_id='YOUR ACCESS ID',
        aws_secret_access_key='YOUR ACCESS KEY',
        region_name='YOUR REGION NAME'
    )