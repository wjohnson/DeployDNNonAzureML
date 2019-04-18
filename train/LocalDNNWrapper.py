import os
# Load the Azure ML SDK Packages
from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import ScriptRunConfig
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Experiment

svc_pr_password = os.environ.get("AZUREML_PASSWORD")
tenant = os.environ.get("TENANT_ID")
serviceprin = os.environ.get("APPID")
sub = os.environ.get("SUBSCRIPTION")
rg = os.environ.get("RESOURCE_GROUP")
wrkspc = os.environ.get("WORKSPACE_NAME")
wrkspc_loc = os.environ.get("WORKSPACE_LOCATION")
exp_name = os.environ.get("EXPERIMENT_NAME")


# This Service Principal needs to have access to the resource group
svc_pr = ServicePrincipalAuthentication(
    tenant_id=tenant,
    service_principal_id=serviceprin,
    service_principal_password=svc_pr_password
)
# Assumes the workspace already exists
ws = Workspace.get(
    subscription_id=sub,
    resource_group=rg,
    name=wrkspc,
    auth=svc_pr
)
# Attach Experiment

exp = Experiment(workspace=ws, name=exp_name)
print(exp.name, exp.workspace.name, sep='\n')

# Editing a run configuration property on-fly.
run_config_user_managed = RunConfiguration()
run_config_user_managed.environment.python.user_managed_dependencies = True

print("Submitting an experiment.")
src = ScriptRunConfig(source_directory='./train', script='LocalDNN.py', run_config=run_config_user_managed)
run = exp.submit(src)

run.wait_for_completion(show_output=True)