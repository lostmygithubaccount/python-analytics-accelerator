# Python analytics accelerator

***A composable data system in a Python package.***

![layers](img/layers.png)

This project uses:

1. **query UI**: Ibis (Python dataframe code and/or SQL)
2. **query engine**: DuckDB and ClickHouse (local and remote)
3. **storage**: Delta Lake tables (local and/or cloud storage)

You can swap out your query engine(s) or storage format(s) as needed, mixing and matching as needed in a **data mesh** fashion. You can also use composable query UIs in other languages like `dplyr` in R, though this project is Python-focused.

> [!CAUTION]
> This accelerator is not necessarily production-ready, but could be a good starting point. For now, it is primarily intended as an educational resource.

## setup

Get up and running in 4 commands.

Install:

```bash
pip install python-analytics-accelerator
```

> [!TIP]
> This makes the `acc` CLI available as long as you have a Python environment with the package installed active. Type `acc` in your terminal to see available commands.

>
Initialize:

```bash
acc init
```

> [!TIP]
> Edit the `config.py` file to the GitHub repository and PyPI package you want to analyze.

> [!IMPORTANT]
> You must edit the `.env` to add your GitHub token or otherwise set `GH_TOKEN` as an environment variable.
>
> You can use `gh auth token` to print your GitHub token if you have the GitHub CLI installed.

Ingest from external sources:

```bash
acc ingest
```

Run ETL:

```bash
acc run
```

Open dashboard:

```bash
acc dashboard
```

## development

Clone and change into the repository:

```bash
gh repo clone lostmygithubaccount/python-analytics-accelerator
cd python-analytics-accelerator
```

Install:

```bash
pip install -r requirements.txt
```

Format your code:

```bash
ruff format .
```

## contributing

Work in progress, contributions welcome. Consider opening an issue for discussion or reaching out in these early days.
