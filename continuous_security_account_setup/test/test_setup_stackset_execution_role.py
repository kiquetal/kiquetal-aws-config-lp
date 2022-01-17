import boto3
from continuous_security_account_setup.account_bootstrap import setup_stackset_execution_role

deployment_account_id = "309735675305"

iam_client = boto3.Session(profile_name="Deployment1", region_name="us-east-1").client("iam")

setup_stackset_execution_role(iam_client, deployment_account_id)
