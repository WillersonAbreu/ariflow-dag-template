from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from airflow.models.variable import Variable


TENANT_ID: str = Variable.get('TENANT_ID')
PRINCIPAL_ID: str = Variable.get('PRINCIPAL_ID')
PRINCIPAL_PASSWORD: str = Variable.get('PRINCIPAL_PASSWORD')
WORKSPACE_NAME: str = Variable.get('WORKSPACE_NAME')
SUBSCRIPTION_ID: str = Variable.get('SUBSCRIPTION_ID')
RESOURCE_GROUP: str = Variable.get('RESOURCE_GROUP')


def build_azure_service_principal_authentication() -> ServicePrincipalAuthentication:
        service_principal = ServicePrincipalAuthentication(
            tenant_id=TENANT_ID,
            service_principal_id=PRINCIPAL_ID,
            service_principal_password=PRINCIPAL_PASSWORD
        )
        return service_principal

def build_azureml_workspace() -> Workspace:
    azureml_workspace = Workspace.get(
        auth=build_azure_service_principal_authentication(),
        name=WORKSPACE_NAME,
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP
    )
    return azureml_workspace