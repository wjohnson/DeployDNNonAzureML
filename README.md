# Introduction 
TODO: A sample project to train and deploy, via Azure DevOps, a Deep Learning model used in image classification.

# Metrics Being Logged
1.	Accuracy is measured as...
1.  Batch Size

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

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