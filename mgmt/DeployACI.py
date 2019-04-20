import os, json, datetime, sys
from Workspace import get_Workspace
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.core.authentication import ServicePrincipalAuthentication

# Get workspace
ws = get_Workspace()

# Get the Image to deploy details
with open("./script-outputs/image.json") as f:
    config = json.load(f)

image_name = config['image_name']
image_version = config['image_version']

images = Image.list(workspace=ws)
image, = (m for m in images if m.version==image_version and m.name == image_name)
print('From image.json, Image used to deploy webservice on ACI: {}\nImage Version: {}\nImage Location = {}'.format(image.name, image.version, image.image_location))

aci_config = AciWebservice.deploy_configuration(
    cpu_cores=1, 
    memory_gb=1, 
    tags={'area': "diabetes", 'type': "regression"},
    description='A sample description'
)

aci_service_name='aciwebservice'+ datetime.datetime.now().strftime('%m%d%H')

service = Webservice.deploy_from_image(
    deployment_config=aci_config,
    image=image,
    name=aci_service_name,
    workspace=ws
)

service.wait_for_deployment()
print('Deployed ACI Webservice: {} \nWebservice Uri: {}'.format(service.name, service.scoring_uri))


aci_webservice = {}
aci_webservice['aci_name'] = service.name
aci_webservice['aci_url'] = service.scoring_uri
with open('./script-outputs/aci_webservice.json', 'w') as outfile:
  json.dump(
      obj = aci_webservice,
      fp = outfile
    )