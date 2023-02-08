"""Main entry when running the summarizer as a package.

Example:

    GITHUB_TOKEN=xxx python -m summarizer --gh-repo issues --gh-label release/2023-01
"""
import sys
from .args import parse_args
from .summary import summary, render


def main():
    """Run the summarizer."""
    args = parse_args()
    notes = summary(args)
    print(render(notes, args.template))
    sys.exit(0)


main()
