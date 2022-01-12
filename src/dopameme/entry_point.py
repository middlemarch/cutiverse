# Standard
import os
import argparse
import errno
import logging
import pkg_resources
import sys
from logging.config import dictConfig

# Third Party
from log_color import ColorFormatter, ColorStripper

# Project
from dopameme.cute import run
from dopameme import constants

LOG = logging.getLogger(__name__)

# Setup the version string globally
try:
    pkg_version = f"%(prog)s {pkg_resources.get_distribution('dopameme').version}"
except pkg_resources.DistributionNotFound:
    pkg_version = "%(prog)s Development"
except Exception:
    pkg_version = "%(prog)s Unknown"


def logging_init(level, logfile=None, verbose=False):
    """
    Given the log level and an optional logging file location, configure
    all logging.
    """
    # Get logging related arguments & the configure logging
    if logfile:
        logfile = os.path.abspath(logfile)

    # Don't bother with a file handler if we're not logging to a file
    handlers = ["console", "filehandler"] if logfile else ["console"]

    # If the main logging level is any of these, set librarys to WARNING
    lib_warn_levels = ("DEBUG", "INFO", "WARNING")

    # The base logging configuration
    BASE_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "ConsoleFormatter": {
                "()": ColorFormatter,
                "format": "%(levelname)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "FileFormatter": {
                "()": ColorStripper,
                "format": ("%(levelname)-8s: %(asctime)s '%(message)s' " "%(name)s:%(lineno)s"),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG" if verbose else level,
                "class": "logging.StreamHandler",
                "formatter": "ConsoleFormatter",
            },
        },
        "loggers": {
            "dopameme": {
                "handlers": handlers,
                "level": "DEBUG" if verbose else level,
                "propagate": False,
            },
            "requests": {
                "handlers": handlers,
                "level": "WARNING" if level in lib_warn_levels else level,
                "propagate": False,
            },
        },
    }

    # If we have a log file, modify the dict to add in the filehandler conf
    if logfile:
        BASE_CONFIG["handlers"]["filehandler"] = {
            "level": "DEBUG" if verbose else level,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": logfile,
            "formatter": "FileFormatter",
        }

    # Setup the loggers
    dictConfig(BASE_CONFIG)


def cli():
    parser = argparse.ArgumentParser(
        description="Find amazingly cute things!",
    )
    parser.add_argument(
        "-n",
        "--noun",
        action="store",
        dest="noun",
        default=None,
        help="Use a specific noun instead of randomly selecting one",
    )
    parser.add_argument(
        "-V", "--version", dest="version", action="version", version=pkg_version, help="Display the version number."
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        help="Logging level for command output.",
        dest="log_level",
    )
    parser.add_argument(
        "-L", "--logfile", dest="logfile", default=None, help="Location to place a log of the process output"
    )
    parsed_args = parser.parse_args()
    logging_init(parsed_args.log_level, logfile=parsed_args.logfile)
    LOG.info("Welcome to Dopameme!\n#c<%s>", constants.KITTEN)
    run(noun=parsed_args.noun)
    LOG.debug("#g<\u2713> Complete!.")
    sys.exit(0)


def main():
    try:
        cli()
    except KeyboardInterrupt:
        # Write a nice message to stderr
        sys.stderr.write("\n\033[91m\u2717 Operation canceled by user.\033[0m\n")
        sys.exit(errno.EINTR)
