import json
import os
import subprocess

import pytest

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def read_data():
    def wrapper(path):
        file_path = os.path.join(dir_path, "data", path)
        with open(file_path, "r") as f:
            return json.load(f)

    return wrapper


@pytest.fixture(scope="session", autouse=True)
def cython_setup():
    subprocess.call("python setup.py build_ext --inplace ", shell=True)
