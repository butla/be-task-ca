import subprocess
import uvicorn

from be_task_ca import common

def start():
    uvicorn.run("be_task_ca.app:app", host="0.0.0.0", port=common.APP_PORT, reload=True)


def auto_format():
    subprocess.call(["black", "be_task_ca"])


def run_linter():
    subprocess.call(["flake8", "be_task_ca"])


def run_tests():
    subprocess.call(["pytest", "-v"])


def create_dependency_graph():
    subprocess.call(["pydeps", "be_task_ca", "--cluster"])


def check_types():
    subprocess.call(["mypy", "be_task_ca"])
