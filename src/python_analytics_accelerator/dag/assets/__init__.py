from dagster import load_assets_from_modules

from python_analytics_accelerator.dag.assets import bronze, silver, gold
from python_analytics_accelerator.dag.config import BRONZE, SILVER, GOLD

# load assets
bronze_modules = [bronze]
bronze_assets = load_assets_from_modules(bronze_modules, group_name=BRONZE)

silver_modules = [silver]
silver_assets = load_assets_from_modules(silver_modules, group_name=SILVER)

gold = [gold]
gold_assets = load_assets_from_modules(gold, group_name=GOLD)

# all assets
assets = bronze_assets + silver_assets + gold_assets
