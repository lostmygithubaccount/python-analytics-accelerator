import re
import ibis
import dagster
import ibis.selectors as s


# silver functions
def preprocess(t):
    """Common preprocessing steps from silver assets"""

    # ensure unique records
    t = t.distinct(on=~s.c("loaded_at"), keep="first").order_by("loaded_at")

    return t


def postprocess(t):
    """Common postprocessing steps for silver assets"""

    # ensure consistent column casing
    t = t.rename("snake_case")

    return t


# silver data assets
@dagster.asset()
def silver_pypi_downloads(bronze_pypi_downloads):
    """Silver PyPI downloads data."""

    def transform(t):
        # udfs
        @ibis.udf.scalar.python
        def clean_version(version: str, patch: bool = True) -> str:
            pattern = r"(\d+\.\d+\.\d+)" if patch else r"(\d+\.\d+)"
            match = re.search(pattern, version)
            if match:
                return match.group(1)
            else:
                return version

        return t

    silver_pypi_downloads = (
        bronze_pypi_downloads.pipe(preprocess).pipe(transform).pipe(postprocess)
    )
    return silver_pypi_downloads


@dagster.asset()
def silver_gh_commits(bronze_gh_commits):
    """Silver GitHub commits data."""

    def transform(t):
        t = t.unpack("node").unpack("author").rename("snake_case")
        t = t.order_by(ibis._["committed_date"].desc())
        t = t.mutate(total_commits=ibis._.count().over(rows=(0, None)))
        return t

    silver_gh_commits = (
        bronze_gh_commits.pipe(preprocess).pipe(transform).pipe(postprocess)
    )
    return silver_gh_commits


@dagster.asset()
def silver_gh_issues(bronze_gh_issues):
    """Silver GitHub issues data."""

    def transform(t):
        issue_state = (
            ibis.case().when(ibis._["is_closed"], "closed").else_("open").end()
        )

        t = t.unpack("node").unpack("author").rename("snake_case")
        t = t.order_by(ibis._["created_at"].desc())
        t = t.mutate(is_closed=(ibis._["closed_at"] != None))
        t = t.mutate(total_issues=ibis._.count().over(rows=(0, None)))
        t = t.mutate(state=issue_state)
        t = (
            t.mutate(
                is_first_issue=(
                    ibis.row_number().over(
                        ibis.window(group_by="login", order_by=t["created_at"])
                    )
                    == 0
                )
            )
            .relocate("is_first_issue", "login", "created_at")
            .order_by(t["created_at"].desc())
        )
        return t

    silver_gh_issues = (
        bronze_gh_issues.pipe(preprocess).pipe(transform).pipe(postprocess)
    )
    return silver_gh_issues


@dagster.asset()
def silver_gh_prs(bronze_gh_prs):
    """Silver GitHub pull request (PR) data."""

    def transform(t):
        pull_state = (
            ibis.case()
            .when(ibis._["is_merged"], "merged")
            .when(ibis._["is_closed"], "closed")
            .else_("open")
            .end()
        )

        t = t.unpack("node").unpack("author").rename("snake_case")
        t = t.order_by(ibis._["created_at"].desc())
        t = t.mutate(is_merged=(ibis._["merged_at"] != None))
        t = t.mutate(is_closed=(ibis._["closed_at"] != None))
        t = t.mutate(total_pulls=ibis._.count().over(rows=(0, None)))
        # to remove bots
        # t = t.filter(
        #    ~(
        #        (ibis._.login == "ibis-squawk-bot")
        #        | (ibis._.login == "pre-commit-ci")
        #        | (ibis._.login == "renovate")
        #    )
        # )
        t = t.mutate(state=pull_state)
        t = t.mutate(
            merged_at=ibis._["merged_at"].cast("timestamp")
        )  # TODO: temporary fix

        # add first pull by login
        t = (
            t.mutate(
                is_first_pull=(
                    ibis.row_number().over(
                        ibis.window(group_by="login", order_by=t["created_at"])
                    )
                    == 0
                )
            )
            .relocate("is_first_pull", "login", "created_at")
            .order_by(t["created_at"].desc())
        )
        return t

    silver_gh_prs = bronze_gh_prs.pipe(preprocess).pipe(transform).pipe(postprocess)
    return silver_gh_prs


@dagster.asset()
def silver_gh_forks(bronze_gh_forks):
    """Silver GitHub forks data."""

    def transform(t):
        t = t.unpack("node").unpack("owner").rename("snake_case")
        t = t.order_by(ibis._["created_at"].desc())
        t = t.mutate(total_forks=ibis._.count().over(rows=(0, None)))
        return t

    silver_gh_forks = bronze_gh_forks.pipe(preprocess).pipe(transform).pipe(postprocess)
    return silver_gh_forks


@dagster.asset()
def silver_gh_stars(bronze_gh_stars):
    """Silver GitHub stargazers data."""

    def transform(t):
        t = t.unpack("node").rename("snake_case")
        # TODO: fix
        t = t.order_by(ibis._["starred_at"].desc())
        t = t.mutate(company=ibis._["company"].fillna("Unknown"))
        t = t.mutate(total_stars=ibis._.count().over(rows=(0, None)))
        return t

    silver_gh_stars = bronze_gh_stars.pipe(preprocess).pipe(transform).pipe(postprocess)
    return silver_gh_stars


@dagster.asset()
def silver_gh_watchers(bronze_gh_watchers):
    """Silver GitHub watchers data."""

    def transform(t):
        t = t.unpack("node").rename("snake_case")
        # TODO: fix this
        t = t.order_by(ibis._["updated_at"].desc())
        t = t.mutate(total_t=ibis._.count().over(rows=(0, None)))
        t = t.order_by(ibis._["updated_at"].desc())
        return t

    silver_gh_watchers = (
        bronze_gh_watchers.pipe(preprocess).pipe(transform).pipe(postprocess)
    )
    return silver_gh_watchers
