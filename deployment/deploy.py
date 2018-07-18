#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Deployment script for the various environments"""

import argparse
from contextlib import contextmanager
import logging
import os
from pathlib import Path
import shlex
import subprocess
from typing import Union


logger = logging.getLogger(__name__)


def _execute_command(cmd, working_dir, timeout=None, env=None):
    process_environment = os.environ.copy()
    process_environment.update(env if env is not None else {})
    logger.debug("Executing {!r}...".format(cmd))
    try:
        command_response = subprocess.run(
            shlex.split(cmd),
            cwd=working_dir,
            check=True,
            timeout=timeout,  # seconds
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=process_environment
        )
        logger.debug(command_response.stdout)
        logger.debug(command_response.stderr)
        return command_response
    except subprocess.CalledProcessError as exc:
        logger.error(exc.stdout)
        logger.error(exc.stderr)


def execute_git_command(cmd: str, base_dir: Path, timeout: Union[int, None]=3):
    return _execute_command(
        cmd="git {}".format(cmd) if not cmd.startswith("git") else cmd,
        working_dir=str(base_dir),
        timeout=timeout
    )


def execute_django_command(cmd: str, project_dir: Path, python_command: str,
                           env: Union[dict, None]):
    return _execute_command(
        cmd="{python} manage.py {cmd}".format(python=python_command, cmd=cmd),
        working_dir=str(project_dir),
        env=env
    )


def execute_pip_command(cmd: str, working_dir: Path, pip_command: str):
    command = "{pip} {cmd}".format(pip=pip_command, cmd=cmd)
    return _execute_command(cmd=command, working_dir=str(working_dir))


def get_env_vars(path):
    env_file_path = Path(path).expanduser()
    env = {}
    with env_file_path.open() as fh:
        for line in fh:
            key, value = line.replace("export", "").strip().partition("=")[::2]
            if key != "":
                env[key] = value.replace('"', "").replace("'", "")
    return env


def deploy_to_dev(repo_base: Path, args):
    print("Deploying to `dev` environment...")
    git_remote = "origin"
    git_branch = "dev"
    env_vars = get_env_vars(args.env_file)
    logger.debug("Loaded environment variables: {}".format(env_vars))
    logger.debug("Pulling latest code from the `dev` branch...")
    execute_git_command("checkout {}".format(git_branch), repo_base)
    execute_git_command(
        "pull {remote} {branch}".format(remote=git_remote, branch=git_branch),
        repo_base,
        timeout=None
    )
    logger.debug("Updating dependencies...")
    execute_pip_command(
        "install -r production.txt",
        repo_base / "requirements",
        pip_command=args.pip_command
    )
    logger.debug("Processing django migrations...")
    django_project_dir = repo_base / "smbportal"
    execute_django_command(
        "migrate", django_project_dir, args.python_command, env=env_vars)
    logger.debug("Updating translations...")
    execute_django_command(
        "compilemessages",
        django_project_dir,
        args.python_command,
        env=env_vars
    )


def deploy_to_staging(args):
    logger.debug("Deploying to `staging` environment...")
    logger.debug("Pulling latest code from the `master` branch...")
    logger.debug("Processing django migrations...")
    logger.debug("Updating translations...")
    logger.debug("Reloading wsgi server...")
    logger.debug("Running tests...")
    logger.debug("Verifying server security...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "environment",
        help="name of the environment to deploy to"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true"
    )
    parser.add_argument(
        "--python-command",
        default="python",
        help="Command used to launch the python interpreter. Defaults to "
             "%(default)r"
    )
    parser.add_argument(
        "--pip-command",
        default="pip",
        help="Command used to launch pip. Defaults to %(default)r"
    )
    parser.add_argument(
        "-e",
        "--env-file",
        default="~/smb-portal.env",
        help="Path to file with env variables to use. Defaults to %(default)r"
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING)
    handler = {
        "dev": deploy_to_dev,
    }.get(args.environment)
    repo_base = Path(os.path.abspath(__file__)).parent.parent
    handler(repo_base, args)
    print("Done!")
