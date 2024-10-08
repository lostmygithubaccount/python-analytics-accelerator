# imports
from python_analytics_accelerator.config import (
    GH_PRS_TABLE,
    GH_FORKS_TABLE,
    GH_STARS_TABLE,
    GH_ISSUES_TABLE,
    GH_COMMITS_TABLE,
    GH_WATCHERS_TABLE,
)
from python_analytics_accelerator.catalog import Catalog
from python_analytics_accelerator.etl.extract import (
    gh_prs as extract_gh_prs,
    gh_forks as extract_gh_forks,
    gh_stars as extract_gh_stars,
    gh_issues as extract_gh_issues,
    gh_commits as extract_gh_commits,
    gh_watchers as extract_gh_watchers,
)
from python_analytics_accelerator.etl.transform import (
    gh_prs as transform_gh_prs,
    gh_forks as transform_gh_forks,
    gh_stars as transform_gh_stars,
    gh_issues as transform_gh_issues,
    gh_commits as transform_gh_commits,
    gh_watchers as transform_gh_watchers,
)


# functions
def main():
    # instantiate catalog
    catalog = Catalog()

    # extract
    extract_gh_prs_t = extract_gh_prs()
    extract_gh_forks_t = extract_gh_forks()
    extract_gh_stars_t = extract_gh_stars()
    extract_gh_issues_t = extract_gh_issues()
    extract_gh_commits_t = extract_gh_commits()
    extract_gh_watchers_t = extract_gh_watchers()

    # data validation
    for t in [
        extract_gh_prs_t,
        extract_gh_forks_t,
        extract_gh_stars_t,
        extract_gh_issues_t,
        extract_gh_commits_t,
        extract_gh_watchers_t,
    ]:
        assert (
            t.count().to_pyarrow().as_py() > 0
        ), f"No extracted data for {t.get_name()}"

    # transform
    transform_gh_prs_t = transform_gh_prs(extract_gh_prs_t)
    transform_gh_forks_t = transform_gh_forks(extract_gh_forks_t)
    transform_gh_stars_t = transform_gh_stars(extract_gh_stars_t)
    transform_gh_issues_t = transform_gh_issues(extract_gh_issues_t)
    transform_gh_commits_t = transform_gh_commits(extract_gh_commits_t)
    transform_gh_watchers_t = transform_gh_watchers(extract_gh_watchers_t)

    # data validation
    for t in [
        transform_gh_prs_t,
        transform_gh_forks_t,
        transform_gh_stars_t,
        transform_gh_issues_t,
        transform_gh_commits_t,
        transform_gh_watchers_t,
    ]:
        assert (
            t.count().to_pyarrow().as_py() > 0
        ), f"No transformed data for {t.get_name()}"

    # load
    catalog.write_table(transform_gh_prs_t, GH_PRS_TABLE)
    catalog.write_table(transform_gh_forks_t, GH_FORKS_TABLE)
    catalog.write_table(transform_gh_stars_t, GH_STARS_TABLE)
    catalog.write_table(transform_gh_issues_t, GH_ISSUES_TABLE)
    catalog.write_table(transform_gh_commits_t, GH_COMMITS_TABLE)
    catalog.write_table(transform_gh_watchers_t, GH_WATCHERS_TABLE)
