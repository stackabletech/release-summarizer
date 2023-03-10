"""Command line argument handling for the summarizer."""
from argparse import Namespace, ArgumentParser, Action
import os
from .version import __version__

REPOS = [
    "operator-rs",
    "commons-operator",
    "secret-operator",
    "listener-operator",
    "airflow-operator",
    "hive-operator",
    "hdfs-operator",
    "kafka-operator",
    "opa-operator",
    "nifi-operator",
    "spark-k8s-operator",
    "superset-operator",
    "trino-operator",
    "zookeeper-operator",
    "issues",
]


class EnvDefault(Action):
    """Argparse helper action that reads a parameter from environment
    if not provided on the command line.
    """

    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super().__init__(default=default, required=required,
                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def parse_args() -> Namespace:
    """Parse summarizer command line arguments."""
    parser = ArgumentParser(
        description="Summarize release information."
    )
    parser.add_argument(
        "-o",
        "--gh-owner",
        help="GitHub token owner. Reads the USER env var by default.",
        action=EnvDefault, envvar='USER')
    parser.add_argument(
        "-g",
        "--gh-org",
        help="Organization name. Default: stackable.",
        default="stackabletech",
    )
    parser.add_argument(
        "-t", "--gh-token",
        help="GitHub token. Reads GITHUB_TOKEN env var by default.",
        action=EnvDefault, envvar='GITHUB_TOKEN')
    parser.add_argument(
        "-r",
        "--gh-repo",
        help="Repositories to scrape.",
        nargs="+",
        default=REPOS
    )
    parser.add_argument(
        "-d",
        "--gh-debug",
        help="Debug GitHub api calls.",
        action='store_true'
    )
    parser.add_argument(
        "-l",
        "--gh-label",
        help="Filter issues by GitHub labels.",
        nargs="+",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--gh-state",
        help="Filter issues by GitHub state. Default: closed.",
        default='closed'
    )
    parser.add_argument(
        "-j",
        "--template",
        help="Template name.",
        default='release-notes.adoc.j2'
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display application version.",
        action='version',
        version=__version__)

    return parser.parse_args()
