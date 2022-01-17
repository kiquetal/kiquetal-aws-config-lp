from continuous_security_account_setup.ou_bootstrap import (
    create_management_ou,
    create_app_dev_ou,
)
from continuous_security_account_setup.organizations import org_root_id


def create_org(master_account_boto_session, email_name, email_host):
    """Top level call to create the OUs and accounts we need for the exercises"""
    org_client = master_account_boto_session.client("organizations")
    sts_client = master_account_boto_session.client("sts")

    root_id = org_root_id(org_client)

    deployment_account_id = create_management_ou(org_client, sts_client, root_id, email_name, email_host)
    create_app_dev_ou(org_client, sts_client, root_id, email_name, email_host, deployment_account_id)



def create_org_cloudtrail_deployment_role(iam_client, deployment_account_id):
    trust_policy = """{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
             "AWS": "arn:aws:iam::{deployment_account_id}:root"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    """
    permission_policy = """{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "cloudtrail:*",
                    "cloudwatch:*",
                    "cloudformation:*",
                    "iam:*",
                    "kms:*",
                    "s3:*"
                ],
                "Resource": [
                    "*"
                ],
                "Effect": "Allow"
            }
        ]
    }"""
    _ = iam_client.create_role(
        RoleName="TrailDeploymentRole",
        AssumeRolePolicyDocument=trust_policy,
    )
    waiter = iam_client.get_waiter("role_exists")
    waiter.wait(
        RoleName="TrailDeploymentRole",
        WaiterConfig={"Delay": 15, "MaxAttempts": 123},
    )
    _ = iam_client.put_role_policy(
        RoleName="TrailDeploymentRole",
        PolicyName="TrailDeploymentRole",
        PolicyDocument=permission_policy,
    )