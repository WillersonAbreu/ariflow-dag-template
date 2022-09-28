from mlflow.entities.run import Run
import mlflow


def check_status(task_instance, submitted_job_run_id):
    try:
        executed_job: Run = mlflow.get_run(run_id=submitted_job_run_id)
        mlflow_job_status = executed_job.info.status
    except Exception:
        print(f'Warning: {ex}')

    print(f'SUBMITTED JOB: {mlflow_job_status}')

    if mlflow_job_status == 'FINISHED':
        task_instance.set_state(state='success')
        return True

    if mlflow_job_status == 'FAILED':
        task_instance.set_state(state='failed')
        raise ValueError('O experimento falhou')

    if task_instance != 'SCHEDULED':
        try:
            task_instance.set_state(state='running')
            return False
        except Exception as ex:
            print(f'Warning: {ex}')