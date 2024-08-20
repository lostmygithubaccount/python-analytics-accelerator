# imports
import os
import ibis

from datetime import datetime
from python_analytics_accelerator.config import (
    DATA_DIR,
    RAW_DATA_DIR,
    RAW_DATA_GH_DIR,
)

# set extracted_at timestamp
extracted_at = datetime.utcnow().isoformat()


# functions
def add_extracted_at(t):
    """Add extracted_at column to table."""

    # add extracted_at column and relocate it to the first position
    t = t.mutate(extracted_at=ibis.literal(extracted_at)).relocate("extracted_at")

    return t


def constraints(t):
    """Check common constraints for extracted tables."""

    assert t.count().to_pyarrow().as_py() > 0, "table is empty!"

    return t


# extract data assets
def gh_commits():
    """Extract GitHub commits data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "commits.*.json")
    gh_commits = ibis.read_json(data_glob)

    # add extracted_at column
    github_commits = gh_commits.pipe(add_extracted_at).pipe(constraints)

    return github_commits


def gh_issues():
    """Extract GitHub issues data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "issues.*.json")
    gh_issues = ibis.read_json(data_glob)

    # add extracted_at column
    github_issues = gh_issues.pipe(add_extracted_at).pipe(constraints)

    return github_issues


def gh_prs():
    """Extract GitHub pull request (PR) data."""

    # read in raw data
    data_glob = os.path.join(
        DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "pullRequests.*.json"
    )
    gh_prs = ibis.read_json(data_glob)

    # add extracted_at column
    github_prs = gh_prs.pipe(add_extracted_at).pipe(constraints)

    return github_prs


def gh_forks():
    """Extract GitHub forks data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "forks.*.json")
    gh_forks = ibis.read_json(data_glob)

    # add extracted_at column
    github_forks = gh_forks.pipe(add_extracted_at).pipe(constraints)

    return github_forks


def gh_stars():
    """Extract GitHub stargazers data."""

    # read in raw data
    data_glob = os.path.join(
        DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "stargazers.*.json"
    )
    gh_stars = ibis.read_json(data_glob)

    # add extracted_at column
    github_stars = gh_stars.pipe(add_extracted_at).pipe(constraints)

    return github_stars


def gh_watchers():
    """Extract GitHub watchers data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "watchers.*.json")
    gh_watchers = ibis.read_json(data_glob)

    # add extracted_at column
    github_watchers = gh_watchers.pipe(add_extracted_at).pipe(constraints)

    return github_watchers
