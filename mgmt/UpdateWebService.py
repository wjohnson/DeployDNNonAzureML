import argparse
import time
from azureml.core.webservice import Webservice
from azureml.core.image import Image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("service",help="The service you're updating.")
    parser.add_argument("image",help="The image id and version number you'd like to update to.")
    args = parser.parse_args()

    service_name = args.service
    image_name = args.image
    # Import stored down here to prevent having to get the workspace if just checking out help
    from Workspace import get_Workspace
    ws =get_Workspace()
    # Retrieve existing service
    service = Webservice(name = service_name, workspace = ws)

    # point to a different image
    new_image = Image(workspace = ws, id=image_name)

    # Update the image used by the service
    service.update(image = new_image)
    time.sleep(5)
    print(service.state)