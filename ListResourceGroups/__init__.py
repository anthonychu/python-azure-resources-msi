import json
import logging
import os

import azure.functions as func
from azure.common.credentials import get_azure_cli_credentials
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from msrestazure.azure_active_directory import MSIAuthentication


def main(req: func.HttpRequest) -> func.HttpResponse:
    if "MSI_ENDPOINT" in os.environ:
        credentials = MSIAuthentication()
    else:
        credentials, *_ = get_azure_cli_credentials()

    subscription_client = SubscriptionClient(credentials)
    subscription = next(subscription_client.subscriptions.list())
    subscription_id = subscription.subscription_id

    client = ResourceManagementClient(credentials, subscription_id)

    resource_groups = [g.name for g in client.resource_groups.list()]

    return func.HttpResponse(json.dumps(resource_groups), mimetype="application/json")
