import os
import pytest
from airflow.models import DagBag


def get_dags():
    dag_bag = DagBag(include_examples=False)
    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]


def strip_path_prefix(path):
    return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))


APPROVED_TAGS = {"example"}  # Adjust based on your tagging requirements


# @pytest.mark.parametrize(
#     "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
# )
# def test_import_errors(dag_id, dag, fileloc):
#     print("test import")
#     assert not dag.import_errors, f"{dag_id} in {fileloc} has import errors:\n{dag.import_errors}"


@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_tags(dag_id, dag, fileloc):
    assert dag.tags, f"{dag_id} in {fileloc} has no tags"
    if APPROVED_TAGS:
        assert not set(dag.tags) - APPROVED_TAGS


@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_task_trigger_rules(dag_id, dag, fileloc):
    assert dag.tasks, f"{dag_id} in {fileloc} has no tasks"
    for task in dag.tasks:
        assert (
            task.trigger_rule == "all_success"
        ), f"{task} in {dag_id} has the trigger rule {task.trigger_rule}"