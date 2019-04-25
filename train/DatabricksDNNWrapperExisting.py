from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps.databricks_step import DatabricksStep
import os, json
# Load the Azure ML SDK Packages
from azureml.core.runconfig import RunConfiguration, PyPiLibrary
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
    "databricksexist", 
    inputs=None, 
    outputs=None,
    existing_cluster_id="0423-222152-ogres40", 
    spark_version=None, 
    node_type=None, 
    num_workers=None, 
    min_workers=None, 
    max_workers=None, 
    spark_env_variables=None, 
    spark_conf=None, 
    notebook_path="/Shared/sample", 
    notebook_params=None, 
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
    pypi_libraries=None, 
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


pipeline_run1 = Experiment(ws, 'dbrtest').submit(pipeline1)
pipeline_run1.wait_for_completion()

#store information about the run
if not os.path.exists("./script-outputs"):
    os.makedirs("./script-outputs")

with open("./script-outputs/run.json", 'w') as fp:
    json.dump({
        "runid":pipeline_run1.id, 
        "experiment": pipeline_run1.experiment.name,
        "workspace":ws.name, 
        "modelname":"MODEL_BASIC_1.h5"},
    fp)