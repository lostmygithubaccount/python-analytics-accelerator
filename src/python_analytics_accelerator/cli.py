import os
import typer
import httpx
import subprocess

from python_analytics_accelerator.etl import main as etl_main
from python_analytics_accelerator.ingest import main as ingest_main
from python_analytics_accelerator.catalog import delta_table_path

from python_analytics_accelerator.config import (
    DATA_DIR,
    RAW_DATA_DIR,
    GH_PRS_TABLE,
    GH_FORKS_TABLE,
    GH_STARS_TABLE,
    GH_ISSUES_TABLE,
    GH_COMMITS_TABLE,
    GH_WATCHERS_TABLE,
)

TYPER_KWARGS = {
    "no_args_is_help": True,
    "add_completion": False,
    "context_settings": {"help_option_names": ["-h", "--help"]},
}
app = typer.Typer(help="acc", **TYPER_KWARGS)
clean_app = typer.Typer(help="Clean the data lake.", **TYPER_KWARGS)

## add subcommands
app.add_typer(clean_app, name="clean")

## add subcommand aliases
app.add_typer(clean_app, name="c", hidden=True)


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
    tables = [
        GH_PRS_TABLE,
        GH_FORKS_TABLE,
        GH_STARS_TABLE,
        GH_ISSUES_TABLE,
        GH_COMMITS_TABLE,
        GH_WATCHERS_TABLE,
    ]
    for table in tables:
        if not os.path.exists(delta_table_path(table)):
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
    generate_creds: bool = typer.Option(
        False,
        "--generate-creds",
        "-c",
        help="generate GitHub credentials",
        show_default=True,
    ),
):
    """Initialize the project."""
    if not os.path.exists("config.py"):
        typer.echo("creating config.py...")
        with open("config.py", "w") as f:
            f.write(f'GH_REPO = "{gh_repo}"\n')
            f.write(f'PYPI_PACKAGE = "{pypi_package}"\n')
    else:
        typer.echo("found config.py:\n")
        with open("config.py") as f:
            typer.echo(f.read())

    if not os.path.exists(".env"):
        typer.echo("creating .env...")
        with open(".env", "w") as f:
            f.write('GITHUB_TOKEN="your_token_here"\n')

        if generate_creds:
            try:
                cmd = 'echo "GITHUB_TOKEN = \\"$(gh auth token)\\"" > .env'
                typer.echo(f"running: {cmd}...")
                subprocess.call(cmd, shell=True)
            except Exception as e:
                typer.echo(f"error: {e}")

    else:
        typer.echo("found .env")


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
@app.command("etl", hidden=True)
def run(
    job_name: str = typer.Option(
        "all_assets",
        "--job-name",
        "-j",
        help="Name of the job to run",
        show_default=True,
    ),
    override: bool = typer.Option(
        False, "--override", "-o", help="Override checks", show_default=True
    ),
):
    """Run ETL."""

    # ensure data is ingested
    if not override and not check_ingested_data_exists():
        return

    try:
        etl_main()
    except KeyboardInterrupt:
        typer.echo("stopping...")
    except Exception as e:
        typer.echo(f"error: {e}")


@app.command()
@app.command("dash", hidden=True)
@app.command("metrics", hidden=True)
def dashboard():
    """Open the dashboard."""

    # ensure data is ingested
    if not check_ingested_data_exists():
        return

    # ensure data lake exists
    if not check_data_lake_exists():
        return

    if not os.path.exists("dashboard.py"):
        url = "https://raw.githubusercontent.com/lostmygithubaccount/python-analytics-accelerator/main/dashboard.py"

        response = httpx.get(url)
        if response.status_code != 200:
            typer.echo(f"error: {response.text}")
            return
        dashboard_code = response.text

        typer.echo("creating dashboard.py...")
        with open("dashboard.py", "w") as f:
            f.write(dashboard_code)
    else:
        typer.echo("found dashboard.py")

    typer.echo("opening dashboard...")

    cmd = "shiny run dashboard.py -b"
    subprocess.call(cmd, shell=True)


@clean_app.command("lake")
def clean_lake(
    override: bool = typer.Option(
        False, "--override", "-o", help="Override checks", show_default=True
    ),
):
    """Clean the data lake."""
    # ensure the data lake exists
    if not override and not check_data_lake_exists():
        return

    tables = [
        GH_PRS_TABLE,
        GH_FORKS_TABLE,
        GH_STARS_TABLE,
        GH_ISSUES_TABLE,
        GH_COMMITS_TABLE,
        GH_WATCHERS_TABLE,
    ]

    for table in tables:
        cmd = f"rm -rf {delta_table_path(table)}/"
        typer.echo(f"running: {cmd}...")
        subprocess.call(cmd, shell=True)


@clean_app.command("ingest")
def clean_ingest(
    override: bool = typer.Option(
        False, "--override", "-o", help="Override checks", show_default=True
    ),
    confirm: bool = typer.Option(
        True, "--confirm", "-c", help="Confirm deletion", show_default=True
    ),
):
    """Clean the raw data."""
    # ensure the data ingested exists
    if not override and not check_ingested_data_exists():
        return

    if confirm:
        typer.confirm("Are you sure you want to delete the ingested data?", abort=True)

    cmd = f"rm -rf {os.path.join(DATA_DIR, RAW_DATA_DIR)}/"
    typer.echo(f"running: {cmd}...")
    subprocess.call(cmd, shell=True)


@clean_app.command("all")
def clean_all():
    """Clean all the data."""
    clean_lake()
    clean_ingest()


if __name__ == "__main__":
    typer.run(app)
