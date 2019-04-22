docker pull %REGISTRY_NAME%.azurecr.io/%IMAGE_VERSION%
REM Interactive mode
REM docker run -it %REGISTRY_NAME%.azurecr.io/mnist-h5-img:4 /bin/bash

REM To deploy locally, may have to 1.) Stop all services 2.) Restart Docker
REM (In powershell) docker ps -a -q | ForEach { docker stop $_ }
REM Web Service locally - Can't have anything else interferring with the left hand side.  Right is the container port 
REM docker run -d -p 127.0.0.1:8000:5001 %REGISTRY_NAME%.azurecr.io/%IMAGE_VERSION%
