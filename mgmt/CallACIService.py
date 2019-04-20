import numpy as np
from Workspace import get_Workspace
import os, json, datetime, sys
import numpy as np
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice

def load_sample_data():
    with open("./tests/data/mnist_test.json", 'r') as fp:
        data = np.array(json.load(fp = fp))
    return data

def call_using_aml(service_name):
    service= Webservice(name = service_name, workspace =ws)
    
    try:   
        prediction = service.run(input_data = test_sample)
        print(prediction)
        return prediction
    except Exception as e:
        result = str(e)
        print(result)
        raise Exception('ACI service is not working as expected')

if __name__ == "__main__":
    data = load_sample_data()
    test_sample = json.dumps({'data': data.tolist()})
    test_sample = bytes(test_sample,encoding = 'utf8')
    
    # Get workspace
    ws = get_Workspace()

    # Get the ACI Details
    with open("./script-outputs/aci_webservice.json") as f:
        config = json.load(f)

    print("Calling via Azure ML SDK")
    _ = call_using_aml(service_name = config['aci_name'])