import os

from Workspace import get_Workspace

from azureml.core.compute import DatabricksCompute, ComputeTarget
from azureml.exceptions import ComputeTargetException

access_token = os.environ.get("DATABRICKS_TOKEN")
databricks_workspace = os.environ.get("DATABRICKS_WORKSPACE")
rg = os.environ.get("RESOURCE_GROUP")

ws = get_Workspace()

try:
    databricks_compute = ComputeTarget(workspace=ws, name=databricks_workspace)
    print("Databricks Compute Target of {} already exists".format(databricks_workspace))
except ComputeTargetException:
    print("The Compute Target of {} will be created.".format(databricks_compute))

    databricks_config = DatabricksCompute.attach_configuration(
        resource_group=rg, 
        workspace_name=databricks_workspace,
        access_token=access_token
    )

    databricks_compute = ComputeTarget.attach(
        workspace=ws, 
        name=databricks_workspace, 
        attach_configuration = databricks_config
    )

    databricks_compute.wait_for_completion(show_output=True)