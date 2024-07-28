# imports
import ibis
import ibis.selectors as s

from python_analytics_accelerator.dag.resources import Catalog

# connect to catalog
catalog = Catalog()

# get source tables
pulls_t = catalog.table("gold_gh_prs").cache()
stars_t = catalog.table("gold_gh_stars").cache()
forks_t = catalog.table("gold_gh_forks").cache()
issues_t = catalog.table("gold_gh_issues").cache()
commits_t = catalog.table("gold_gh_commits").cache()
downloads_t = catalog.table("gold_pypi_downloads").cache()
