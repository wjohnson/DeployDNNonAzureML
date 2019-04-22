# Introduction 
TODO: A sample project to train and deploy, via Azure DevOps, a Deep Learning model used in image classification.

# Metrics Being Logged
1.	Accuracy is measured as...
1.  Batch Size

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

## Order of Scripts
1. `train/LocalDNNWrapper.py` calls the `train/LocalDNN.py` to train the model.
   * Generates `script-outputs/run.json`
1. `mgmt/RegisterModel.py` takes the last run and registers it in the Azure ML Workspace.
   * Uses `script-outputs/run.json`
   * Generates `script-outputs/model.json`
1. `mgmt/CreateImage.py` takes the registered model and creates an image.
   * Uses `script-outputs/model.json`
   * Uses `score/score.py` 
   * Generates `score/dependencies.yml`
   * Generates `script-outputs/image.json`
1. `mgmt/DeployACI.py` takes the registered model and creates an image.
   * Uses `script-outputs/image.json`
1. `mgmt/CallACIService.py` to test the model.
   * Uses `tests/data/mnist_test.json` to load pre-processed image data.
1. **TODO**: Validate that the model is performing above threshold
1. `mgmt\PrepareIOTEdge.py` to create the deployment script for IoT Edge
   * Uses `iot-edge-template.json` and does a find and replace on several parameters.
1. Run these commands on the az cli

    az login
    az extension add --name azure-cli-iot-ext
    az account set --subscription $subscription_id
    az iot edge set-modules --device-id $iot_device_id --hub-name $iot_hub_name --content deployment.json

1. You've completed the pipeline!


## Environment Variables Needed

    set TENANT_ID=
    set APPID=
    set AZUREML_PASSWORD=
    set SUBSCRIPTION=
    set RESOURCE_GROUP=
    set WORKSPACE_NAME=
    set WORKSPACE_LOCATION=
    set EXPERIMENT_NAME=
    set DATABRICKS_TOKEN=
    set DATABRICKS_WORKSPACE=
    set MODEL_NAME=


# Setup

1. Azure DevOps
1. Azure Databricks
1. Azure IoT Edge Runtime

## Azure DevOps

## Azure Databricks

## Azure IoT Edge Runtime

[Register an IoT Device](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-register-device-portal)

[Install IoT Edge on Linux](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge-linux)

[Azure ML on IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-deploy-machine-learning)

* While the service is in preview, process identification isn't available.
* Have to add this for management and listening urls to `sudo nano /etc/iotedge/config.yaml` .  Get correct IP Address with `ifconfig` and grab `docker0` interface url.

    connect:
      management_uri: "http://172.17.0.1:15580"
      workload_uri: "http://172.17.0.1:15581"
    listen:
      management_uri: "http://172.17.0.1:15580"
      workload_uri: "http://172.17.0.1:15581"

* Then you'll have to run `export IOTEDGE_HOST="http://172.17.0.1:15580"`
* Add the same export to `/etc/environment` to make it permanent.
* Restart the device `sudo systemctl restart iotedge`


* Az CLI work

    az login
    az extension add --name azure-cli-iot-ext
    az account set --subscription $subscription_id
    az iot edge set-modules --device-id $iot_device_id --hub-name $iot_hub_name --content deployment.json


# TO LOOKUP
* Templated builds - Here are the four steps that need to happen
* Run Pipeline - View YAML