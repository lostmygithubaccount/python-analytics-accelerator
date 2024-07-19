import dagster


# gold data assets
@dagster.asset()
def gold_pypi_downloads(silver_pypi_downloads):
    """Gold PyPI downloads data."""
    return silver_pypi_downloads


@dagster.asset()
def gold_gh_commits(silver_gh_commits):
    """Gold GitHub commits data."""
    return silver_gh_commits


@dagster.asset()
def gold_gh_issues(silver_gh_issues):
    """Gold GitHub issues data."""
    return silver_gh_issues


@dagster.asset()
def gold_gh_prs(silver_gh_prs):
    """Gold GitHub pull request (PR) data."""
    return silver_gh_prs


@dagster.asset()
def gold_gh_forks(silver_gh_forks):
    """Gold GitHub forks data."""
    return silver_gh_forks


@dagster.asset()
def gold_gh_stars(silver_gh_stars):
    """Gold GitHub stargazers data."""
    return silver_gh_stars


@dagster.asset()
def gold_gh_watchers(silver_gh_watchers):
    """Gold GitHub watchers data."""
    return silver_gh_watchers
