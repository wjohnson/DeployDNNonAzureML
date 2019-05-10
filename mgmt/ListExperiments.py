import os
import azureml
from azureml.core import Experiment
from azureml.core import Workspace

from Workspace import get_Workspace, svc_pr


if __name__ == "__main__":
    ws = Workspace.from_config(path = "./script-outputs", auth = svc_pr)
    script_folder = "."
    experiments_in_workspace = list(ws.experiments.values())

    print("There were {exp_count} experiments in the workspace of {ws_name}".format(
        exp_count = len(experiments_in_workspace),
        ws_name = ws.name
        )
    )
    for exp in experiments_in_workspace:
        print(
            "Experiment: {}".format(exp.name),
            "Runs: {}".format(len(list(exp.get_runs())))
        )
