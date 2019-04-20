import os, json
from Workspace import get_Workspace

from azureml.core.conda_dependencies import CondaDependencies 
from azureml.core.image import ContainerImage
from azureml.core.model import Model


if __name__ == "__main__":

    ws = get_Workspace()
    with open("./script-outputs/model.json", 'r') as fp:
        config = json.load(fp)
    model_name = config['model_name']
    model_version = config['model_version']

    # Grab the model object from the list of available models
    model_list = Model.list(workspace=ws)
    model, = (m for m in model_list if m.version==model_version and m.name==model_name)
    print('Model picked: {} \nModel Description: {} \nModel Version: {}'.format(model.name, model.description, model.version))


    dependencies = CondaDependencies()
    dependencies.add_conda_package("numpy")
    dependencies.add_conda_package("matplotlib")
    dependencies.add_conda_package("scikit-learn")
    dependencies.add_conda_package("tensorflow")
    dependencies.add_conda_package("keras")
    dependencies.add_conda_package("scikit-image")
    dependencies.add_pip_package("pynacl==1.2.1")

    with open("./score/dependencies.yml","w") as f:
        f.write(dependencies.serialize_to_string())

    os.chdir("./score")
    image_config = ContainerImage.image_configuration(
        execution_script = "score.py",
        runtime = "python",
        conda_file = "dependencies.yml",
        description = "Image with keras model on small mnist data",
        tags = {"data": "mnist", "type": "classification"}
    )


    # Image Name can only include alphanumeric or '.' and '-'
    image = ContainerImage.create(
        name = "mnist-h5-img",
        models = [model], # this is the registered model object
        image_config = image_config,
        workspace = ws)

    image.wait_for_creation(show_output = True)