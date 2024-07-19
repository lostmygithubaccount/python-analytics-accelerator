import os
import ibis
import gcsfs
import logging as log

from dotenv import load_dotenv
from dagster import ConfigurableIOManager
from python_analytics_accelerator.dag.config import DATA_DIR, BRONZE

## configure logging
log.basicConfig(level=log.INFO)

## load environment variables
load_dotenv()


# define data catalog
class Catalog:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        self.con = ibis.duckdb.connect()

    def list_groups(self):
        return sorted(
            [
                d
                for d in os.listdir(self.data_dir)
                if not (d.startswith("_") or d.startswith("."))
            ]
        )

    def list_tables(self, group):
        return sorted(
            [d.split(".")[0] for d in os.listdir(os.path.join(self.data_dir, group))]
        )

    def table(self, table_name, group_name=None):
        if group_name is None:
            group_name = table_name.split("_")[0].upper()
        return self.con.read_delta(
            os.path.join(DATA_DIR, group_name, f"{table_name}.delta")
        )


# define IO manager(s)
class DeltaLakeIOManager(ConfigurableIOManager):
    """
    Manage tables as Delta Lake tables.
    """

    extension: str = "delta"
    bucket: str = os.getenv("BUCKET")
    cloud: bool = (
        True if os.getenv("BUCKET") is not None and (len(bucket) != 0) else False
    )
    base_path: str = f"gs://{bucket}/{DATA_DIR}" if cloud else DATA_DIR

    def handle_output(self, context, obj):
        """Called on the output of an asset."""
        if self.cloud:
            log.info(f"Using bucket: {self.bucket}")
            fs = gcsfs.GCSFileSystem()
            ibis.get_backend(obj).register_filesystem(fs)

        group_name, dirname, filename = self._get_paths(context)
        if not self.cloud:
            os.makedirs(dirname, exist_ok=True)
        output_path = os.path.join(dirname, filename)

        partition_by = ["loaded_at"] if group_name == BRONZE else None
        mode = "append" if group_name == BRONZE else "overwrite"
        obj.to_delta(output_path, partition_by=partition_by, mode=mode)

    def load_input(self, context):
        """Called on the input of an asset."""
        if self.cloud:
            log.info(f"Using bucket: {self.bucket}")
            fs = gcsfs.GCSFileSystem()
            ibis.get_backend().register_filesystem(fs)

        group_name, dirname, filename = self._get_paths(context)
        input_path = os.path.join(dirname, filename)
        return ibis.read_delta(input_path)

    def _get_paths(self, context):
        """Get relevant paths for the asset."""
        group_name = context.step_context.job_def.asset_layer.asset_graph.get(
            context.asset_key
        ).group_name
        dirname = os.path.join(self.base_path, group_name)
        filename = f"{context.asset_key.path[-1]}.{self.extension}"
        return group_name, dirname, filename


# set default IO manager
resources = {"io_manager": DeltaLakeIOManager()}
