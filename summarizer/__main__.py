"""Main entry when running the summarizer as a package.

Example:

    GITHUB_TOKEN=xxx python -m summarizer --gh-repo issues --gh-label release/2023-01
"""
from .main import main

main()
