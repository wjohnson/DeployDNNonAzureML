import sys, os
from pathlib import Path

if __name__ == "__main__":
    parentdir = str(Path(os.path.abspath(__file__)).parents[1])
    sys.path.append(parentdir)

    from mgmt.Workspace import svc_pr

    from azureml.core.compute import DatabricksCompute, ComputeTarget
    from azureml.exceptions import ComputeTargetException
    from azureml.core import Workspace

    access_token = os.environ.get("DATABRICKS_TOKEN")
    databricks_workspace = os.environ.get("DATABRICKS_WORKSPACE")
    rg = os.environ.get("RESOURCE_GROUP")

    ws = Workspace.from_config(auth=svc_pr)

    try:
        print("Trying to create databricks compute...")
        databricks_compute = ComputeTarget(workspace=ws, name=databricks_workspace)
        print("Databricks Compute Target of {} already exists".format(databricks_workspace))
    except ComputeTargetException:
        print("The Compute Target of {} will be created.".format(databricks_workspace))

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
