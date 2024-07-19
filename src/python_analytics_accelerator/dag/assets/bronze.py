import os
import ibis
import dagster

from datetime import datetime
from python_analytics_accelerator.dag.config import (
    DATA_DIR,
    RAW_DATA_DIR,
    RAW_DATA_GH_DIR,
    RAW_DATA_PYPI_DIR,
)

# set loaded_at timestamp
loaded_at = datetime.utcnow().isoformat()


# bronze functions
def add_loaded_at(t):
    """Add loaded_at column to table."""

    # add loaded_at column and relocate it to the first position
    t = t.mutate(loaded_at=ibis.literal(loaded_at)).relocate("loaded_at")

    return t


def constraints(t):
    """Check common constraints for bronze tables."""

    assert t.count().to_pyarrow().as_py() > 0, "table is empty!"

    return t


# bronze data assets
@dagster.asset
def bronze_pypi_downloads():
    """Bronze PyPI downloads data."""

    # read in raw data
    data_glob = os.path.join(
        DATA_DIR, RAW_DATA_DIR, RAW_DATA_PYPI_DIR, "*downloads*.parquet"
    )
    bronze_pypi_downloads = ibis.read_parquet(data_glob)
    bronze_pypi_downloads = bronze_pypi_downloads.order_by(ibis._["count"].desc())

    # add loaded_at column
    bronze_pypi_downloads = bronze_pypi_downloads.pipe(add_loaded_at).pipe(constraints)

    return bronze_pypi_downloads


@dagster.asset
def bronze_gh_commits():
    """Bronze GitHub commits data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "commits.*.json")
    bronze_gh_commits = ibis.read_json(data_glob)

    # add loaded_at column
    bronze_github_commits = bronze_gh_commits.pipe(add_loaded_at).pipe(constraints)

    return bronze_github_commits


@dagster.asset
def bronze_gh_issues():
    """Bronze GitHub issues data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "issues.*.json")
    bronze_gh_issues = ibis.read_json(data_glob)

    # add loaded_at column
    bronze_github_issues = bronze_gh_issues.pipe(add_loaded_at).pipe(constraints)

    return bronze_github_issues


@dagster.asset
def bronze_gh_prs():
    """Bronze GitHub pull request (PR) data."""

    # read in raw data
    data_glob = os.path.join(
        DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "pullRequests.*.json"
    )
    bronze_gh_prs = ibis.read_json(data_glob)

    # add loaded_at column
    bronze_github_prs = bronze_gh_prs.pipe(add_loaded_at).pipe(constraints)

    return bronze_github_prs


@dagster.asset
def bronze_gh_forks():
    """Bronze GitHub forks data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "forks.*.json")
    bronze_gh_forks = ibis.read_json(data_glob)

    # add loaded_at column
    bronze_github_forks = bronze_gh_forks.pipe(add_loaded_at).pipe(constraints)

    return bronze_github_forks


@dagster.asset
def bronze_gh_stars():
    """Bronze GitHub stargazers data."""

    # read in raw data
    data_glob = os.path.join(
        DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "stargazers.*.json"
    )
    bronze_gh_stars = ibis.read_json(data_glob)

    # add loaded_at column
    bronze_github_stars = bronze_gh_stars.pipe(add_loaded_at).pipe(constraints)

    return bronze_github_stars


@dagster.asset
def bronze_gh_watchers():
    """Bronze GitHub watchers data."""

    # read in raw data
    data_glob = os.path.join(DATA_DIR, RAW_DATA_DIR, RAW_DATA_GH_DIR, "watchers.*.json")
    bronze_gh_watchers = ibis.read_json(data_glob)

    # add loaded_at column
    bronze_github_watchers = bronze_gh_watchers.pipe(add_loaded_at).pipe(constraints)

    return bronze_github_watchers
