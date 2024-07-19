# configuration file for the data DAG
DAG_MODULE = "python_analytics_accelerator.dag"

CLOUD = False
BUCKET = "python-analytics-accelerator"

DATA_DIR = "datalake"
RAW_DATA_DIR = "_raw"
RAW_DATA_GH_DIR = "github"
RAW_DATA_PYPI_DIR = "pypi"

BRONZE = "bronze"
SILVER = "silver"
GOLD = "gold"
