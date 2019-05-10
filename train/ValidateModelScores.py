import os, sys, json
from pathlib import Path
from azureml.core import Run, Experiment, Workspace

def run_metric_is_better_than_threshold(run_value, threshold_dict):
    """
    Determing if the run value has better performance than the threshold value.

    :param run_value: The containing experiment.
    :type run_value: int or float
    :param threshold_dict: The run id for the run.
    :type threshold_dict: dict("value":int,"direction":("min"|"max"))
    """
    is_better = False

    direction = threshold_dict.get("direction", "").lower()
    threshold_value = threshold_dict["value"]

    if direction == "min":
        is_better = run_value < threshold_value
    elif direction == "max":
        is_better = run_value > threshold_value
    else:
        raise NotImplementedError("The direction of {} is not implemented.".format(direction))

    return is_better


if __name__ == "__main__":
    parentdir = str(Path(os.path.abspath(__file__)).parents[1])
    sys.path.append(parentdir)

    from mgmt.Workspace import svc_pr

    ws = Workspace.from_config(auth = svc_pr)
    # Load supporting run and thresholds
    with open("./script-outputs/run.json", 'r') as fp:
        config = json.load(fp)
    
    with open("./thresholds.json", 'r') as fp:
        thresholds = json.load(fp)

    experiment = Experiment(ws, config["experiment"])
    run = Run(experiment, config["runid"])

    run_metrics = run.get_metrics()

    results = {}
    all_metrics_are_better = True
    for threshold_name, thresh_dict in thresholds.items():

        run_value = run_metrics[threshold_name]
        run_is_better = run_metric_is_better_than_threshold(run_value, thresh_dict)
        results[threshold_name] = {"run_value":run_value,"threshold":thresh_dict,"run_is_better":run_is_better}
        if not run_is_better:
            all_metrics_are_better = False
    
    with open("./script-outputs/validation.json",'w') as fp:
        json.dump(results, fp)
    
    print(json.dumps(results,indent=2))

    if all_metrics_are_better:
        print("Successfully beat all metrics")
        exit(0)
    else:
        print("Failed to beat all metrics")
        exit(1)
    
