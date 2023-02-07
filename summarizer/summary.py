from argparse import Namespace
from ghapi.all import GhApi, paged, print_summary
from urllib.request import Request
from attrs import define
from typing import List
from fastcore.basics import AttrDict
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from importlib import resources


def _noop_debug(req: Request) -> None:
    pass


@define(frozen=True)
class RepoSummary:
    repo: str
    issues: List[AttrDict]


@define(frozen=True)
class Summary:
    label: str
    repo: List[RepoSummary]


def summary(args: Namespace) -> Summary:
    debug = print_summary if args.gh_debug else _noop_debug
    api = GhApi(owner=args.gh_org,
                org=args.gh_org, token=args.gh_token, debug=debug)

    result = []
    for repo in args.gh_repo:
        pages = paged(api.issues.list_for_repo, repo=repo, owner=args.gh_org, filter="all",
                      state=args.gh_state, labels=','.join(args.gh_label))
        issues = []
        for page in pages:
            issues.extend([issue for issue in page])

        result.append(RepoSummary(repo=repo, issues=issues))

    return Summary(label=','.join(args.gh_label), repo=result)


def _jinja_now(format: str) -> str:
    """Helper function to render modification time in generated documents."""
    return datetime.now().strftime(format)  #


def render(summary: Summary, template: str) -> str:
    with resources.path(__package__, template) as template_path:
        template_dir = template_path.parent.joinpath("templates")
        print(template_dir)
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True
        )
        env.globals['now'] = _jinja_now
        t = env.get_template(template)
        return t.render({"summary": summary})
