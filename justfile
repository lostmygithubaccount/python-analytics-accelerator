# justfile

# load environment variables
set dotenv-load

# variables
module := "python_analytics_accelerator.dag"
package := "python-analytics-accelerator"

# aliases
alias fmt:=format
alias app:=dashboard

# list justfile recipes
default:
    just --list

# build
build:
    just clean-dist
    @python -m build

# setup
setup:
    @pip install -r dev-requirements.txt
    just install

# install
install:
    @pip install -e .

# uninstall
uninstall:
    @pip uninstall -y {{package}}

# format
format:
    @ruff format .

# publish-test
release-test:
    just build
    @twine upload --repository testpypi dist/* -u __token__ -p ${PYPI_TEST_TOKEN}

# publish
release:
    just build
    @twine upload dist/* -u __token__ -p ${PYPI_TOKEN}

# clean dist
clean-dist:
    @rm -rf dist

# clean lake
clean-lake:
    @rm -rf datalake/bronze
    @rm -rf datalake/silver
    @rm -rf datalake/gold

# clean raw
clean-raw:
    @rm -rf datalake/raw

# clean data
clean-data:
    just clean-raw
    just clean-lake

# open-dag
open-dag:
    @open http://127.0.0.1:3000/asset-groups

# pres
pres:
    @quarto preview pres.qmd

# dashboard
dashboard:
    @streamlit run metrics.py
