import argparse
import time
import os, sys
from pathlib import Path
from azureml.core.webservice import Webservice
from azureml.core import Image, Workspace

if __name__ == "__main__":
    parentdir = str(Path(os.path.abspath(__file__)).parents[1])
    sys.path.append(parentdir)

    from mgmt.Workspace import svc_pr

    ws = Workspace.from_config(auth = svc_pr)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("service",help="The service you're updating.")
    parser.add_argument("image",help="The image id and version number you'd like to update to.")
    args = parser.parse_args()

    service_name = args.service
    image_name = args.image
    # Import stored down here to prevent having to get the workspace if just checking out help
    
    # Retrieve existing service
    service = Webservice(name = service_name, workspace = ws)

    # point to a different image
    new_image = Image(workspace = ws, id=image_name)

    # Update the image used by the service
    service.update(image = new_image)

    time.sleep(5)
    service._wait_for_operation_to_complete()

    print(service.state)