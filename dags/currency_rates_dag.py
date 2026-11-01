from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
python_path = project_dir / ".venv" / "bin" / "python"
script_path = project_dir / "load_currency.py"

with DAG(
    dag_id="currency_rates_dag",
    start_date=pendulum.datetime(2026,10,30, tz="Europe/Moscow"),
    schedule="0 8 * * *",
    catchup=False,
) as dag:
    load_new_currency = BashOperator(
        task_id="task_1",
        bash_command=f'"{python_path}" "{script_path}"'
    )

    