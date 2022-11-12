import os
import environ


def get_environment_variables(base_dir) -> environ.Env:
    env = environ.Env()
    environ.Env.read_env(os.path.join(base_dir, '.env'))
    return env
