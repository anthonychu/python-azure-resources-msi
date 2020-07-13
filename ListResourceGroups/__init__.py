import json
import logging
import os

import azure.functions as func
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.identity import DefaultAzureCredential


def main(req: func.HttpRequest) -> func.HttpResponse:
    credentials = DefaultAzureCredential()
    subscription_client = SubscriptionClient(credentials)
    subscription = next(subscription_client.subscriptions.list())
    subscription_id = subscription.subscription_id

    client = ResourceManagementClient(credentials, subscription_id)
    resource_groups = [g.name for g in client.resource_groups.list()]

    return func.HttpResponse(json.dumps(resource_groups), mimetype="application/json")
