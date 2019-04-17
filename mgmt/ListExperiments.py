import os
import azureml
from azureml.core import Experiment
from azureml.core import Workspace

from Workspace import get_Workspace


if __name__ == "__main__":
    ws = get_Workspace()
    script_folder = "."
    experiments_in_workspace = ws.experiments

    print("There were {exp_count} experiments in the workspace of {ws_name}".format(
        exp_count = len(experiments_in_workspace),
        ws_name = ws.name
        )
    )
    for exp in experiments_in_workspace:
        print(
            "Experiment: {}".format(exp.name),
            "Runs: {}".format(exp.get_runs())
        )
