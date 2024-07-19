from dagster import Definitions

from python_analytics_accelerator.dag.jobs import jobs
from python_analytics_accelerator.dag.assets import assets
from python_analytics_accelerator.dag.resources import resources

# definitions
defs = Definitions(
    assets=assets,
    resources=resources,
    jobs=jobs,
)
