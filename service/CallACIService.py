import numpy as np
import requests
import argparse
import os, json, datetime, sys
from pathlib import Path
import numpy as np
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.exceptions import WebserviceException

def load_sample_data():
    with open("./tests/data/mnist_test.json", 'r') as fp:
        data = np.array(json.load(fp = fp))
    return data

def call_using_aml(service, input_data):
    try:   
        prediction = service.run(input_data = input_data)
        print(prediction)
        return prediction
    except Exception as e:
        result = str(e)
        print(result)
        raise Exception('ACI service is not working as expected')

def call_using_request_and_service(service, input_data):
    # This is the same code underlying the service.run() method
    headers = {'Content-Type': 'application/json'}
    try:
        service_keys = service.get_keys()
    except WebserviceException as e:
        raise WebserviceException('Error attempting to retrieve service keys for use with scoring:\n'
                                    '{}'.format(e.message))
    headers['Authorization'] = 'Bearer ' + service_keys[0]

    resp = requests.post(service.scoring_uri, headers=headers, data=input_data)

    if resp.status_code == 200:
        print(resp.json())
        return resp.json()
    else:
        raise WebserviceException('Received bad response from service:\n'
                                    'Response Code: {}\n'
                                    'Headers: {}\n'
                                    'Content: {}'.format(resp.status_code, resp.headers, resp.content))

def call_using_request_only(scoring_uri, service_key, input_data):
    # This is the same code underlying the service.run() method
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = 'Bearer ' + service_key

    resp = requests.post(scoring_uri, headers=headers, data=input_data)

    if resp.status_code == 200:
        print(resp.json())
        return resp.json()
    else:
        raise WebserviceException('Received bad response from service:\n'
                                    'Response Code: {}\n'
                                    'Headers: {}\n'
                                    'Content: {}'.format(resp.status_code, resp.headers, resp.content))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri",help="The scoring URI to call")
    parser.add_argument("--key",help="The web service's key")
    parser.add_argument("--aml",help="Switch to use AML Service",action="store_true")
    parser.add_argument("--amlreq",help="Switch to use Requests but still rely on the AML Service",action="store_true")
    args = parser.parse_args()

    data = load_sample_data()
    test_sample = json.dumps({'data': data.tolist()})
    test_sample = bytes(test_sample,encoding = 'utf8')
    
    # Get workspace
    if args.aml or args.amlreq:
        parentdir = str(Path(os.path.abspath(__file__)).parents[1])
        sys.path.append(parentdir)
        from mgmt.Workspace import svc_pr

        ws = Workspace.from_config(auth = svc_pr)
        # Get the ACI Details
        with open("./script-outputs/aci_webservice.json") as f:
            config = json.load(f)
        
        service_name = config['aci_name']
        service= Webservice(name = service_name, workspace =ws)
        print("Scoring URI:{}".format(service.scoring_uri))
        print("Key:{}".format(service.get_keys()[0]))

    
    if args.aml:
        print("Calling via Azure ML SDK")
        _ = call_using_aml(service, test_sample)

    if args.amlreq:
        print("Calling via Requests library with service data")
        _ = call_using_request_and_service(service, test_sample)

    if (args.uri is not None) and (args.key is not None):
        print("Calling via Requests library only")
        _ = call_using_request_only(args.uri, args.key, test_sample)