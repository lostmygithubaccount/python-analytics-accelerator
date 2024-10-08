# imports
import os
import ibis

from python_analytics_accelerator.config import CLOUD, BUCKET, DATA_DIR


# functions
def delta_table_filename(table_name: str) -> str:
    return f"{table_name}.delta"


def delta_table_path(table_name: str) -> str:
    return os.path.join(DATA_DIR, delta_table_filename(table_name))


def read_table(table_name: str) -> ibis.Table:
    if CLOUD:
        import gcsfs

        fs = gcsfs.GCSFileSystem()
        ibis.get_backend().register_filesystem(fs)

        table_path = f"gs://{BUCKET}/{delta_table_path(table_name)}"
    else:
        table_path = delta_table_path(table_name)

    return ibis.read_delta(table_path)


def write_table(t: ibis.Table, table_name: str) -> None:
    if CLOUD:
        import gcsfs

        fs = gcsfs.GCSFileSystem()
        ibis.get_backend().register_filesystem(fs)

        table_path = f"gs://{BUCKET}/{delta_table_path(table_name)}"
    else:
        table_path = delta_table_path(table_name)

    t.to_delta(
        table_path,
        mode="overwrite",
        partition_by=["extracted_at"],
    )


# classes
class Catalog:
    def list_tables(self):
        return [
            d
            for d in os.listdir(DATA_DIR)
            if not (d.startswith("_") or d.startswith("."))
        ]

    def table(self, table_name):
        return read_table(table_name)

    def write_table(self, t, table_name):
        write_table(t, table_name)
