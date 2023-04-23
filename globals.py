import os
import docker

DOCKER_CLIENT = docker.from_env()

ABSOLUTE_PATH = os.path.dirname(__file__)
DATA_DIR = os.path.join(ABSOLUTE_PATH, "data")
DATA_FILE = os.path.join(DATA_DIR, "data.json")
os.makedirs(DATA_DIR, exist_ok=True)

CONTAINERS_COUNT = 7
