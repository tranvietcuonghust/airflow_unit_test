from airflow import DAG
from airflow.operators.python import ExternalPythonOperator, PythonOperator
from datetime import datetime
from airflow.models import Variable

APPROVED_TAGS = {"example"}
def test_dag_tags():
    assert dag.tags, "DAG has no tags"
    assert not set(dag.tags) - APPROVED_TAGS, "DAG tags are not within approved set"


def test_task_trigger_rules():
    for task in dag.tasks:
        assert task.trigger_rule == "all_success", "Task has a trigger rule other than 'all_success'"


def _extract_stock_yfinance():
    import yfinance as yf
    print(yf.download("AAPL", start="2020-12-01", end="2020-12-31"))
    appl = yf.Ticker("AAPL")
    appl.get_shares_full(start="2020-12-01", end="2020-12-31")

def _print_age(age):
    print(f"Hello you are {age} years old.")
dag = DAG(
    dag_id="my_simple_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # Use schedule_interval instead of schedule for clarity
    catchup=False,
    tags=['examples'],
)

user_name = Variable.get("user_name")
user_age = 30

test_dag_tags_task = PythonOperator(
    task_id="test_dag_tags",
    python_callable=test_dag_tags,
    dag=dag,
)

test_task_trigger_rules_task = PythonOperator(
    task_id="test_task_trigger_rules",
    python_callable=test_task_trigger_rules,
    dag=dag,
)


extract_stock_old_yfinance = ExternalPythonOperator(
    task_id="extract_stock_old_yfinance",
    python_callable=_extract_stock_yfinance,
    python="/home/airflow/yfinance_venv/venv1/bin/python",
    dag=dag,
)

extract_stock_new_yfinance = ExternalPythonOperator(
    task_id="extract_stock_new_yfinance",
    python_callable=_extract_stock_yfinance,
    python="/home/airflow/yfinance_venv/venv2/bin/python",
    dag=dag,
)

my_function = ExternalPythonOperator(
    task_id="my_function",
    python_callable=_print_age,
    op_kwargs={"age": user_age},
    python="/home/airflow/yfinance_venv/venv1/bin/python",  # Consistent with extract_old
    dag=dag,
)

test_dag_tags_task>> extract_stock_old_yfinance
test_task_trigger_rules_task >> extract_stock_old_yfinance
extract_stock_old_yfinance >> extract_stock_new_yfinance >> my_function

