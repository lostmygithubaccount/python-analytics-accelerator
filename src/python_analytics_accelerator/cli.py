import typer
import subprocess

from python_analytics_accelerator.ingest import main as ingest_main
from python_analytics_accelerator.dag.config import DAG_MODULE

TYPER_KWARGS = {
    "no_args_is_help": True,
    "add_completion": False,
    "context_settings": {"help_option_names": ["-h", "--help"]},
}
app = typer.Typer(help="acc", **TYPER_KWARGS)


@app.command()
def ingest():
    """Ingest source data."""
    try:
        ingest_main()
    except KeyboardInterrupt:
        typer.echo("stopping...")

    except Exception as e:
        typer.echo(f"error: {e}")


@app.command()
def gui():
    """Start the dagster webserver/GUI."""
    cmd = f"dagster dev -m {DAG_MODULE}"
    subprocess.call(cmd, shell=True)


@app.command()
def run(
    job_name: str = typer.Option(
        "all_assets",
        "--job-name",
        "-j",
        help="Name of the job to run",
        show_default=True,
    ),
):
    """Run ETL."""
    cmd = f"dagster job execute -j {job_name} -m {DAG_MODULE}"
    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    typer.run(app)
