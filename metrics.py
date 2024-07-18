# imports
import ibis

import streamlit as st
import plotly.express as px

from dotenv import load_dotenv
from datetime import datetime, timedelta

from python_analytics_accelerator.dag.resources import Catalog

# options
## load .env
load_dotenv()

## streamlit config
st.set_page_config(layout="wide")

## configure Ibis connections
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

ddb_con = ibis.duckdb.connect()

## catalog config
catalog = Catalog(con=ddb_con)


# use precomputed data
pulls = catalog.table("gold_gh_prs")
stars = catalog.table("gold_gh_stars")
forks = catalog.table("gold_gh_forks")
issues = catalog.table("gold_gh_issues")
commits = catalog.table("gold_gh_commits")

# display header stuff
with open("readme.md") as f:
    readme_code = f.read()

f"""
{readme_code}
"""


with open("metrics.py") as f:
    metrics_code = f.read()

with st.expander("Show source code", expanded=False):
    st.code(metrics_code, line_numbers=True, language="python")

"""
---
"""

st.dataframe(stars, use_container_width=True)
