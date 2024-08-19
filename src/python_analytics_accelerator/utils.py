import os
import sys
import logging as log

log.basicConfig(level=log.INFO)


def get_config():
    GH_REPO = None
    PYPI_PACKAGE = None

    try:
        sys.path.append(os.getcwd())
        from config import GH_REPO, PYPI_PACKAGE
    except ImportError:
        log.error("GH_REPO and PYPI_PACKAGE not set in config.py")

    log.info(f"GH_REPO={GH_REPO}")
    log.info(f"PYPI_PACKAGE={PYPI_PACKAGE}")

    assert GH_REPO is not None and len(GH_REPO) > 0, log.error("GH_REPO is not set")
    assert PYPI_PACKAGE is not None and len(PYPI_PACKAGE) > 0, log.error(
        "PYPI_PACKAGE is not set"
    )

    return GH_REPO, PYPI_PACKAGE
