from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.webservice import Webservice
import os, json

# Get workspace
svc_pr_password = os.environ.get("AZUREML_PASSWORD")
tenant = os.environ.get("TENANT_ID")
serviceprin = os.environ.get("APPID")
sub = os.environ.get("SUBSCRIPTION")
rg = os.environ.get("RESOURCE_GROUP")
wrkspc = os.environ.get("WORKSPACE_NAME")

if __name__ == "__main__":
    # This Service Principal needs to have access to the resource group
    svc_pr = ServicePrincipalAuthentication(
        tenant_id=tenant,
        service_principal_id=serviceprin,
        service_principal_password=svc_pr_password
        )
    ws = Workspace.get(
        subscription_id=sub,
        resource_group=rg,
        name=wrkspc,
        auth=svc_pr
    )
    with open('./script-outputs/aci_webservice.json', 'r') as fp:
        config = json.load(fp)
    service_name = config["aci_name"]

    service= Webservice(name = service_name, workspace =ws)

    # Get the ACI Details
    print("Scoring URI:{}".format(service.scoring_uri))
    print("Key:{}".format(service.get_keys()[0]))

