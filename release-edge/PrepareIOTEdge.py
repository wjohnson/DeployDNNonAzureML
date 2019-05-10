import os, json, sys
from pathlib import Path
from azureml.core import Image, Workspace
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt import containerregistry

if __name__ == "__main__":
    parentdir = str(Path(os.path.abspath(__file__)).parents[1])
    sys.path.append(parentdir)
    from mgmt.Workspace import svc_pr

    resource_group_name = os.environ.get("RESOURCE_GROUP")

    ws = Workspace.from_config(path = "./script-outputs", auth = svc_pr)

    module_name = "mnistclassifier"

    # Get the Image to deploy details
    with open("./script-outputs/image.json") as f:
        config = json.load(f)

    image_name = config['image_name']
    image_version = config['image_version']

    images = Image.list(workspace=ws)
    image, = (m for m in images if m.version==image_version and m.name == image_name)

    # Extract Container Registry details
    container_reg = ws.get_details()["containerRegistry"]

    reg_name=container_reg.split("/")[-1]
    container_url = "\"" + image.image_location + "\","
    subscription_id = ws.subscription_id

    print('{}'.format(image.image_location))
    print('{}'.format(reg_name))
    print('{}'.format(subscription_id))


    client = ContainerRegistryManagementClient(ws._auth,subscription_id)
    result= client.registries.list_credentials(resource_group_name, reg_name, custom_headers=None, raw=False)
    username = result.username
    password = result.passwords[0].value


    with open("./iot-edge-template.json", 'r') as deploy_template:
        contents = deploy_template.read()
        contents = contents.replace('__MODULE_NAME', module_name)
        contents = contents.replace('__REGISTRY_NAME', reg_name)
        contents = contents.replace('__REGISTRY_USER_NAME', username)
        contents = contents.replace('__REGISTRY_PASSWORD', password)
        contents = contents.replace('__REGISTRY_IMAGE_LOCATION', image.image_location)

    with open('./script-outputs/deployment.json', 'wt', encoding='utf-8') as output_file:
        output_file.write(contents)