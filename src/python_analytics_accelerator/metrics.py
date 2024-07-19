# imports
import os
import sys
import ibis
import streamlit as st
import ibis.selectors as s
import plotly.express as px

from datetime import datetime, timedelta

from python_analytics_accelerator.dag.resources import Catalog

# options
## path config
sys.path.append(os.getcwd())

## streamlit config
st.set_page_config(layout="wide")

## plotly config
px.defaults.template = "plotly_dark"

# connect to catalog
catalog = Catalog()

# display header stuff
if os.path.exists("readme.md"):
    with open("readme.md") as f:
        readme_code = f.read()

    f"""
    {readme_code}
    """

if os.path.exists("metrics.py"):
    with open("metrics.py") as f:
        metrics_code = f.read()

    with st.expander("Show source code", expanded=False):
        st.code(metrics_code, line_numbers=True, language="python")

"""
---
"""


def gh():
    # connect to data
    with st.spinner("Connecting to data..."):
        # get tables
        pulls = catalog.table("gold_gh_prs").cache()
        stars = catalog.table("gold_gh_stars").cache()
        forks = catalog.table("gold_gh_forks").cache()
        issues = catalog.table("gold_gh_issues").cache()
        commits = catalog.table("gold_gh_commits").cache()

    """
    ## pulls
    """
    st.dataframe(pulls, use_container_width=True)

    """
    ## stars
    """
    st.dataframe(stars, use_container_width=True)

    """
    ## forks
    """
    st.dataframe(forks, use_container_width=True)

    """
    ## issues
    """
    st.dataframe(issues, use_container_width=True)

    """
    ## commits
    """
    st.dataframe(commits, use_container_width=True)


def pypi():
    # connect to data
    with st.spinner("Connecting to data..."):
        # get tables
        downloads = catalog.table("gold_pypi_downloads").cache()

    """
    ## downloads
    """
    st.dataframe(downloads, use_container_width=True)


tabs = st.tabs(["GitHub", "PyPI"])

with tabs[0]:
    gh()

with tabs[1]:
    pypi()
