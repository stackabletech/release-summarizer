"""Main"""
import sys
from .args import parse_args
from .summary import summary, render


def main():
    """Run the summarizer."""
    args = parse_args()
    notes = summary(args)
    print(render(notes, args.template))
    sys.exit(0)
