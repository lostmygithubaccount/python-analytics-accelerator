import os
import typer
import inspect
import subprocess


from python_analytics_accelerator.ingest import main as ingest_main
from python_analytics_accelerator.dag.config import (
    DAG_MODULE,
    DATA_DIR,
    RAW_DATA_DIR,
    BRONZE,
    SILVER,
    GOLD,
)

TYPER_KWARGS = {
    "no_args_is_help": True,
    "add_completion": False,
    "context_settings": {"help_option_names": ["-h", "--help"]},
}
app = typer.Typer(help="acc", **TYPER_KWARGS)


# helper functions
def check_ingested_data_exists() -> bool:
    # check that the ingested data exists
    if not os.path.exists(os.path.join(DATA_DIR, RAW_DATA_DIR)):
        typer.echo("run `acc ingest` first!")
        return False
    return True


def check_project_config_exists() -> bool:
    # check that the project config exists
    if not os.path.exists("config.py"):
        typer.echo("run `acc init` first!")
        return False
    return True


def check_data_lake_exists() -> bool:
    # check that the data lake exists
    for metal in [BRONZE, SILVER, GOLD]:
        if not os.path.exists(os.path.join(DATA_DIR, metal)):
            typer.echo("run `acc run` first!")
            return False
    return True


# commands
@app.command()
def init(
    gh_repo: str = typer.Option(
        "substrait-io/substrait",
        "--gh-repo",
        "-g",
        help="the GitHub repository",
    ),
    pypi_package: str = typer.Option(
        "substrait", "--pypi-package", "-p", help="the PyPI package"
    ),
):
    """Initialize the project."""
    if not os.path.exists(".env"):
        typer.echo("creating .env...")
        with open(".env", "w") as f:
            f.write('GITHUB_TOKEN="your_token_here"\n')
    else:
        typer.echo("found .env")

    if not os.path.exists("config.py"):
        typer.echo("creating config.py...")
        with open("config.py", "w") as f:
            f.write(f'GH_REPO = "{gh_repo}"\n')
            f.write(f'PYPI_PACKAGE = "{pypi_package}"\n')
    else:
        typer.echo("found config.py:\n")
        with open("config.py") as f:
            typer.echo(f.read())


@app.command()
def ingest():
    """Ingest source data."""
    # ensure project config exists
    if not check_project_config_exists():
        return
    try:
        ingest_main()
    except KeyboardInterrupt:
        typer.echo("stopping...")

    except Exception as e:
        typer.echo(f"error: {e}")


@app.command()
def dag():
    """Start the dagster webserver/GUI."""
    # ensure data is ingested
    if not check_ingested_data_exists():
        return

    # start the dagster webserver
    cmd = f"dagster dev -m {DAG_MODULE}"
    subprocess.call(cmd, shell=True)


@app.command()
@app.command("etl", hidden=True)
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

    # ensure data is ingested
    if not check_ingested_data_exists():
        return

    # materialize all assets
    cmd = f"dagster job execute -j {job_name} -m {DAG_MODULE}"
    subprocess.call(cmd, shell=True)


@app.command()
@app.command("dash", hidden=True)
@app.command("metrics", hidden=True)
def dashboard():
    """Open the metrics dashboard."""

    # ensure data is ingested
    if not check_ingested_data_exists():
        return

    # ensure data lake exists
    if not check_data_lake_exists():
        return

    if not os.path.exists("metrics.py"):
        from python_analytics_accelerator import metrics

        metrics_code = inspect.getsource(metrics)
        typer.echo("creating metrics.py...")
        with open("metrics.py", "w") as f:
            f.write(metrics_code)
    else:
        typer.echo("found metrics.py")

    typer.echo("opening dashboard...")

    cmd = "streamlit run metrics.py"
    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    typer.run(app)
