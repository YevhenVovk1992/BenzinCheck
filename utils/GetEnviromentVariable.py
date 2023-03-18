import os
import environ

from pathlib import Path


def get_environment_variables(base_dir: Path) -> environ.Env:
    env = environ.Env()
    environ.Env.read_env(os.path.join(base_dir, '.env'))
    return env
