import os, json,sys
from pathlib import Path
from azureml.core import Workspace
from azureml.core import Run
from azureml.core import Experiment
from azureml.core.model import Model


if __name__ == "__main__":
    parentdir = str(Path(os.path.abspath(__file__)).parents[1])
    sys.path.append(parentdir)

    from mgmt.Workspace import svc_pr

    ws = Workspace.from_config(path = "./script-outputs", auth = svc_pr)

    with open("./script-outputs/run.json", 'r') as fp:
        run_config = json.load(fp)
    run_id = str(run_config["runid"])
    model_name = run_config["modelname"]
    experiment_name = run_config["experiment"]

    working_experiment = ws.experiments.get(experiment_name)

    if working_experiment is None:
        raise AttributeError("The experiment {} is not found in workspace '{}'".format(experiment_name, ws.name))

    print(working_experiment)
    print(run_id)

    run = Run(experiment = working_experiment, run_id = run_id)
    names=run.get_file_names
    print(names())

    print('Run ID for last run: {}'.format(run_id))
    model_local_dir="./model/"
    os.makedirs(model_local_dir,exist_ok=True)

    # Download Model to Project root directory
    run.download_file(name = './outputs/'+model_name,
                        output_file_path = model_local_dir+model_name)
    print('Downloaded model {} to Project root directory'.format(model_name))

    model = Model.register(model_path = model_local_dir+model_name, # this points to a local file
                        model_name = model_name, # this is the name the model is registered as
                        tags = {'area': "mnist", 'type': "classification", 'run_id' : run_id},
                        description="MNIST classifier",
                        workspace = ws)

    print('Model registered: {} \nModel Description: {} \nModel Version: {}'.format(model.name, model.description, model.version))
    with open("./script-outputs/model.json", 'w') as fp:
        json.dump(
            obj = {"model_name":model.name, "model_version":model.version},
            fp = fp
        )
