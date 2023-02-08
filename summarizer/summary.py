"""Build release notes from GitHub issues."""

from argparse import Namespace
from datetime import datetime
from importlib import resources
from typing import List
from urllib.request import Request
from ghapi.all import GhApi, paged, print_summary
from attrs import define
from fastcore.basics import AttrDict
from jinja2 import Environment, FileSystemLoader


def _noop_debug(req: Request) -> None:  # pylint: disable=unused-argument
    pass


@define(frozen=True)
class RepoSummary:  # pylint: disable=too-few-public-methods
    """Release notes summary for a given repository."""
    repo: str
    issues: List[AttrDict]


@define(frozen=True)
class Summary:  # pylint: disable=too-few-public-methods
    """Release notes summary"""
    label: str
    repo: List[RepoSummary]


def summary(args: Namespace) -> Summary:
    """Scrape GitHub repos for issues matching the given label."""
    debug = print_summary if args.gh_debug else _noop_debug
    api = GhApi(owner=args.gh_org,
                org=args.gh_org, token=args.gh_token, debug=debug)

    result = []
    for repo in args.gh_repo:
        pages = paged(api.issues.list_for_repo, repo=repo, owner=args.gh_org, filter="all",
                      state=args.gh_state, labels=','.join(args.gh_label))
        issues = []
        for page in pages:
            issues.extend(list(page))

        result.append(RepoSummary(repo=repo, issues=issues))

    return Summary(label=','.join(args.gh_label), repo=result)


def _jinja_now(fmt: str) -> str:
    """Helper function to render modification time in generated documents."""
    return datetime.now().strftime(fmt)  #


def render(notes: Summary, template: str) -> str:
    """Render release notes with the given template."""
    with resources.path(__package__, template) as template_path:
        template_dir = template_path.parent.joinpath("templates")
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True
        )
        env.globals['now'] = _jinja_now
        tmpl = env.get_template(template)
        return tmpl.render({"summary": notes})
