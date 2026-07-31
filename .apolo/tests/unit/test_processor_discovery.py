from pathlib import Path

import yaml
from apolo_app_types.outputs.utils.discovery import (
    load_app_postprocessor,
    load_app_preprocessor,
)


APPLICATIONS_YAML = Path(__file__).resolve().parents[2] / "applications.yaml"


def _superset_app() -> dict:
    apps = yaml.safe_load(APPLICATIONS_YAML.read_text())
    return next(app for app in apps if app["app_type"] == "superset")


def test_input_processor_name_matches_code() -> None:
    app = _superset_app()
    loaded = load_app_preprocessor(
        app["app_type"],
        app["app_package_name"],
        app["inputs"]["processor"],
    )
    assert loaded is not None, (
        f"inputs.processor {app['inputs']['processor']!r} in applications.yaml "
        f"is not a class in {app['app_package_name']}"
    )


def test_output_processor_name_matches_code() -> None:
    app = _superset_app()
    loaded = load_app_postprocessor(
        app["app_type"],
        app["app_package_name"],
        app["outputs"]["processor"],
    )
    assert loaded is not None, (
        f"outputs.processor {app['outputs']['processor']!r} in applications.yaml "
        f"is not a class in {app['app_package_name']}"
    )
