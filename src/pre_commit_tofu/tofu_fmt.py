from __future__ import annotations

import argparse
import logging
import os
import shlex
import shutil
from collections.abc import Sequence
from subprocess import run

logger = logging.getLogger(__name__)

default_resolution_order = [
    "tofu",
    "terraform",
]


def get_tofu_command_path(resolution_order: Sequence[str] = default_resolution_order) -> str:
    for cmd in resolution_order:
        if cmd_path := shutil.which(cmd):
            return cmd_path
    raise FileNotFoundError(f"Could not find any of {resolution_order}")


def tofu_fmt(filenames: Sequence[str], tofu_command_path: str | None = None) -> int:
    if tofu_command_path is None:
        tofu_command_path = get_tofu_command_path()
    cmd = [tofu_command_path, "fmt", *filenames]
    logger.debug("running: %s", shlex.join(cmd))
    completed_process = run(cmd)
    return completed_process.returncode


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    parser.add_argument(
        "--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level"
    )
    parser.add_argument(
        "--commands",
        default=",".join(default_resolution_order),
        help=f"Comma-separated list of commands to try.  Default: {','.join(default_resolution_order)}",
    )

    args = parser.parse_args(argv)

    log_level = args.log_level or os.environ.get("LOG_LEVEL", "INFO")
    logging.basicConfig(level=log_level)

    tofu_command_path = get_tofu_command_path(resolution_order=args.commands.split(","))

    return tofu_fmt(args.filenames, tofu_command_path=tofu_command_path)


if __name__ == "__main__":
    raise SystemExit(main())
