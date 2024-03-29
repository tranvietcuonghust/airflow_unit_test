from airflow.models import DagBag
import os
def strip_path_prefix(path):
    return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))
def get_dags():
    dag_bag = DagBag(include_examples=False)
    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]

print(get_dags())
