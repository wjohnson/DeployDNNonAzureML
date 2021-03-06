import time
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps.databricks_step import DatabricksStep
import os, json
# Load the Azure ML SDK Packages
from azureml.core.runconfig import RunConfiguration, PyPiLibrary
from azureml.core import Workspace
from azureml.core import ScriptRunConfig
from azureml.core.authentication import ServicePrincipalAuthentication

from msrest.exceptions import AuthenticationError

from azureml.core import Experiment

svc_pr_password = os.environ.get("AZUREML_PASSWORD")
tenant = os.environ.get("TENANT_ID")
serviceprin = os.environ.get("APPID")
sub = os.environ.get("SUBSCRIPTION")
rg = os.environ.get("RESOURCE_GROUP")
wrkspc = os.environ.get("WORKSPACE_NAME")
wrkspc_loc = os.environ.get("WORKSPACE_LOCATION")
exp_name = os.environ.get("EXPERIMENT_NAME")
model_name = os.environ.get("MODEL_NAME")


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



if __name__=="__main__":

    databricks_workspace=os.environ.get("DATABRICKS_WORKSPACE")
    compute_target=ws.compute_targets.get(databricks_workspace)

    dbr_step=DatabricksStep(
    name = "databricks", 
    inputs=None, 
    outputs=None,
    existing_cluster_id=None, 
    spark_version="5.3.x-cpu-ml-scala2.11", 
    node_type="Standard_DS12_v2", 
    num_workers=1, 
    min_workers=None, 
    max_workers=None, 
    spark_env_variables=None, 
    spark_conf=None, 
    notebook_path="/dnn/dbr-example", 
    notebook_params={"model_name": model_name}, 
    python_script_path=None, 
    python_script_params=None, 
    main_class_name=None, 
    jar_params=None, 
    python_script_name=None, 
    source_directory=None, 
    hash_paths=None, 
    run_name=None,
    timeout_seconds=None, 
    runconfig=None, 
    maven_libraries=None, 
    pypi_libraries=[PyPiLibrary(package="azureml-sdk")], 
    egg_libraries=None, 
    jar_libraries=None, 
    rcran_libraries=None, 
    compute_target=compute_target, 
    allow_reuse=False, 
    version=None
)

#what pipeline step to run...preprocessing, feature engineering, etc.
steps = [dbr_step]

pipeline1 = Pipeline(ws, steps)

try:
    pipeline_run1 = Experiment(ws, exp_name).submit(pipeline1)
    pipeline_run1.wait_for_completion()
except AuthenticationError as e:
    print("Authentication Error.  Retrying")

    continue_to_run = True
    retries = 0
    while(continue_to_run):
        if pipeline_run1.get_status() != "Running":
            continue_to_run = False
        else:
            sleep_time = 60
            print("Sleeping for {} minutes".format(sleep_time/60))
            time.sleep(sleep_time)
            retries += 1

        if retries == 10:
            print("Failed after several retries")
            raise e

if pipeline_run1.get_status() == "Failed":
    raise Exception("The Pipeline run failed!  See Azure ML Services.")


# Extract the child runs
child_run = list(pipeline_run1.get_children())[0]

#store information about the run
if not os.path.exists("./script-outputs"):
    os.makedirs("./script-outputs")

with open("./script-outputs/run.json", 'w') as fp:
    json.dump({
        "runid": child_run.id, 
        "parentrunid": pipeline_run1.id,
        "experiment": pipeline_run1.experiment.name,
        "workspace": ws.name, 
        "modelname": model_name},
    fp)