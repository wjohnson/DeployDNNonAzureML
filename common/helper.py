import json


def validate_against_thresholds(scores):
    """
    """
    def print_comparison(metric, thresh, challenge):
        print("{metric}: {thresh}\t{challenge} ".format(
            metric = key, thresh = thresh_value, challenge = challenge_value
            )
        )
    
    # Base case is that the test should pass
    exit_code = 0
    with open("./reference/thresholds.json", 'r') as fp:
        thresholds = json.load(fp)
    
    # Iterate over the keys to examine the threshold values
    for key in thresholds:

        thresh_value = thresholds[key]["value"]
        direction = thresholds[key]["direction"].lower()
        
        if scores.get(key) is None:
            print("The key {key} was missing from the challenger scores".format(key = key))
            exit_code = 1
            break
        
        challenge_value = scores.get(key)["value"]

        if direction == "min":
            print_comparison(key, thresh_value, challenge_value)
        elif direction == "max":
            print_comparison(key, thresh_value, challenge_value)
        else:
            raise NotImplementedError("{key} has not been implemented.".format(key))

    return exit_code
