import os
import pytest
import sys
sys.path.append(os.getcwd())

from common.helper import *

def test_validate_against_thresholds():

    scores = {
    "Accuracy": {"value":0.95, "direction":"Max"},
    "FalsePositives": {"value":0.1, "direction":"Min"}
    }

    exit_code = validate_against_thresholds(scores)

    assert exit_code == 0

def test_validate_against_thresholds_direction_not_existing():

    raise NotImplementedError

def test_validate_against_thresholds_direction_key_in_challenger_missing():

    raise NotImplementedError