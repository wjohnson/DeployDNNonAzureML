# Sample Call:
# python3 simplecall.py --uri http://127.0.0.1:5001/score --key XXXX
import numpy as np
import requests
import argparse
import os, json, datetime, sys

def load_sample_data():
    with open("./tests/data/mnist_test.json", 'r') as fp:
        data = np.array(json.load(fp = fp))
    return data

def call_using_request_only(scoring_uri, service_key, input_data):
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = 'Bearer ' + service_key

    resp = requests.post(scoring_uri, headers=headers, data=input_data)

    if resp.status_code == 200:
        print(resp.json())
        return resp.json()
    else:
        raise Exception('Received bad response from service:\n'
                                    'Response Code: {}\n'
                                    'Headers: {}\n'
                                    'Content: {}'.format(resp.status_code, resp.headers, resp.content))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri",help="The scoring URI to call")
    parser.add_argument("--key",help="The web service's key")
    args = parser.parse_args()

    data = load_sample_data()
    test_sample = json.dumps({'data': data.tolist()})
    test_sample = bytes(test_sample,encoding = 'utf8')

    if (args.uri is not None) and (args.key is not None):
        print("Calling via Requests library only")
        _ = call_using_request_only(args.uri, args.key, test_sample)