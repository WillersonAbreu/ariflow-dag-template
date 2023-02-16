from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.variable import Variable
from airflow.models.taskinstance import TaskInstance
import mlflow
from dags_autoload.autoload import require_module


'''
Contexto raiz da aplicação
Deixar em branco para o ambiente de desenvolvimento
Essa variável será preenchida no momento do deploy para produção com o nome da aplicação atual
'''
__APP_NAME__ = ''
dag_utils = require_module('utils.dag_utils', f'{__APP_NAME__}')
dags_decorator = require_module('decorators.azureml_connect_decorator', f'{__APP_NAME__}')


AZURE_PAT: str = Variable.get('AZURE_PAT')
REPO_ADDRESS = "dev.azure.com/<AZURE-DEVOPS-ORG>/<AZURE-DEVOPS-PROJECT>/_git/<NOME-DO-REPOSITORIO>"
EXPERIMENT_NAME = '<NOME-DO-EXPERIMENTO-NA-AZURE-ML>'
MLFLOW_BACKEND = 'azureml'
MLFLOW_BACKEND_CONFIG = {"COMPUTE": "S-DS3-v2"}

def run_experiment(task_instance: TaskInstance):
    with dags_decorator.AzuremlConnectDecorator() as azureml_connection:
        mlflow.set_experiment(EXPERIMENT_NAME)
        mlflow.set_tracking_uri(uri=azureml_connection.get_mlflow_tracking_uri())
                
        experiment_run = mlflow.projects.run(
            uri=f'https://{AZURE_PAT}@{REPO_ADDRESS}',
            version='main',
            backend=MLFLOW_BACKEND,
            backend_config=MLFLOW_BACKEND_CONFIG,
            synchronous=False 
        )
        
        submitted_job_run_id: str = experiment_run.run_id
        is_finished = False
        while not is_finished:
            is_finished = dag_utils.check_status(task_instance, submitted_job_run_id=submitted_job_run_id)

'''
Dag para rodar seu fluxo
'''
with DAG(
    'nome_da_sua_dag',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    t1 = PythonOperator(
        task_id='seu_task_id',
        python_callable=run_experiment
    )
    
    t1 
