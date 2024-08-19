# imports
import ibis
import ibis.selectors as s

from python_analytics_accelerator.utils import get_config
from python_analytics_accelerator.catalog import Catalog

# get settings from config.py in the cwd
GH_REPO, PYPI_PACKAGE = get_config()

# connect to PyPI data in the ClickHouse Cloud playground
host = "clickpy-clickhouse.clickhouse.com"
port = 443
user = "play"
database = "pypi"

ch_con = ibis.clickhouse.connect(
    host=host,
    port=port,
    user=user,
    database=database,
)

# connect to catalog
catalog = Catalog()

# get source tables
pulls_t = catalog.table("gh_prs").cache()
stars_t = catalog.table("gh_stars").cache()
forks_t = catalog.table("gh_forks").cache()
issues_t = catalog.table("gh_issues").cache()
commits_t = catalog.table("gh_commits").cache()
downloads_t = ch_con.table(
    "pypi_downloads_per_day_by_version_by_installer_by_type_by_country"
).filter(ibis._["project"] == PYPI_PACKAGE)
