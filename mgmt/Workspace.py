from azureml.core import Workspace
import os, json
import azureml.core
import azureml.core

from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import ScriptRunConfig
from azureml.core.authentication import ServicePrincipalAuthentication
import os, json

# Get workspace
# ws = Workspace.from_config()
svc_pr_password = os.environ.get("AZUREML_PASSWORD")
tenant = os.environ.get("TENANT_ID")
serviceprin = os.environ.get("APPID")
sub = os.environ.get("SUBSCRIPTION")
rg = os.environ.get("RESOURCE_GROUP")
wrkspc = os.environ.get("WORKSPACE_NAME")
wrkspc_loc = os.environ.get("WORKSPACE_LOCATION")


# This Service Principal needs to have access to the resource group
svc_pr = ServicePrincipalAuthentication(
    tenant_id=tenant,
    service_principal_id=serviceprin,
    service_principal_password=svc_pr_password
    )

def get_Workspace(create_if_not_exists = False):
    try:
        ws = Workspace.get(
            subscription_id=sub,
            resource_group=rg,
            name=wrkspc,
            auth=svc_pr
        )
    except:
        # this call might take a minute or two.
        if create_if_not_exists:

            ws = Workspace.create(
                subscription_id=sub,
                resource_group=rg,
                name=wrkspc,
                auth=svc_pr,
                location=wrkspc_loc
            )
        else:
            ws = Workspace()
    return ws


if __name__ == "__main__":
    ws = get_Workspace(create_if_not_exists = True)
    
    # print Workspace details
    print(
        "Workspace Name: {}".format(ws.name),
        "Resource Group: {}".format(ws.resource_group),
        "Location: {}".format(ws.location),
        "Subscription ID: {}".format(ws.subscription_id),
        sep = '\n'
        )
    ws.write_config(path = "./", file_name = "config.json")