# imports
import ibis

import streamlit as st
import plotly.express as px

from datetime import datetime, timedelta

from python_analytics_accelerator.dag.resources import Catalog

# options
## streamlit config
st.set_page_config(layout="wide")

## plotly config
px.defaults.template = "plotly_dark"

# connect to data
with st.spinner("Connecting to data..."):
    # connect to catalog
    catalog = Catalog()

    # get tables
    pulls = catalog.table("gold_gh_prs").cache()
    stars = catalog.table("gold_gh_stars").cache()
    forks = catalog.table("gold_gh_forks").cache()
    issues = catalog.table("gold_gh_issues").cache()
    commits = catalog.table("gold_gh_commits").cache()
    downloads = catalog.table("gold_pypi_downloads").cache()

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

"""
## stars
"""

st.dataframe(stars, use_container_width=True)

"""
## downloads
"""

st.dataframe(downloads, use_container_width=True)
