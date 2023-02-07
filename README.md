# Release Summarizer

This package helps with the assembly of release notes for the Stackable Data Platform by scraping repositories for issues or pull-requests marked with certain labels.

# Usage

NOTE: a GitHub token with read access to the repositories is required. This must be available in the environment variable called `GITHUB_TOKEN` or passed explicitely with the `--gh-token` command line parameter.

Example:

    python -m summarizer --gh-label release/2023-01

The example above generates the release notes for the release 2023-01.

For a list of available options run:

    python -m summarizer --help
