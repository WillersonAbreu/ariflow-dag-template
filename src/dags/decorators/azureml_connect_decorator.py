"""Summary:
    Decorator class to open a new context with Azure ML connection.
"""

import importlib
from contextlib import ContextDecorator
from azureml.core import Workspace
decorator_utils = importlib.import_module('<NOME-DO-SEU-REPOSITORIO>.utils.azureml_connect_utils')


class AzuremlConnectDecorator(ContextDecorator):
    """Summary:
    Class that inherits ContextDecorator from Contextlib.
    Returns:
        workspace: Connected Azure ML Workspace.
    """

    def __enter__(self) -> Workspace:
        azureml_workspace = decorator_utils.build_azureml_workspace()
        return azureml_workspace

    def __exit__(self, *exc):
        return False
