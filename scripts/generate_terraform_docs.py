#!/usr/bin/env python3

"""Generate reference documentation for Terraform configs.

Based on: https://github.com/spotlessthoughful/mkdocs-terraform/blob/f5cc78bbd978d1b3a48ff1579e9e9b2003bb4ccd/scripts/generate_terraform_docs.py
"""

# Standard Libraries
import subprocess
from pathlib import Path
from typing import Any

# Third-party Libraries
import yaml
from loguru import logger


def get_nav_item_paths(collection: list[Any]) -> list[str]:
    """Recursively return all of the file paths listed in the `nav` element.

    Args:
        collection (list[Any]): A subset of the mkdocs `nav` element

    Returns:
        A list of relative paths to documentation pages
    """
    items: list[str] = []

    for item in collection:
        if isinstance(item, dict):
            items.extend(get_nav_item_paths(list(item.values())))  # type: ignore[UnknownArgumentType]
        elif isinstance(item, list):
            items.extend(get_nav_item_paths(item))  # type: ignore[UnknownArgumentType]
        else:
            items.append(item)

    return items


def generate_docs_for_project(repo_root_dir: Path, file_path: Path) -> None:
    """Run `terraform-docs` on the given directory.

    Args:
        repo_root_dir (Path): The path to the root of the git repo (where the `mkdocs.yml` file is located)
        file_path (Path): The path to the Terraform project to generate docs for
    """
    module_path: Path = repo_root_dir / file_path.with_suffix("")

    # Return if the file path doesn't represent a directory (relative to the repo root directory)
    if not module_path.is_dir():
        return

    logger.info("Generating '{}'", file_path)

    # Ensure the output directory exists
    output_file: Path = repo_root_dir / "docs" / file_path
    output_file.parent.mkdir(exist_ok=True, parents=True)

    # Run `terraform-docs`
    command: str = f"terraform-docs --output-file {output_file!s} {module_path}"
    logger.debug("Command: {}", command)
    subprocess.run(command, shell=True, check=True)  # noqa: S602


def generate_terraform_docs() -> None:
    """Read `mkdocs.yml` and iterate over each file path listed in the `nav` element."""
    repo_root_dir: Path = Path(__file__).parent.parent
    mkdocs_config_path: Path = repo_root_dir / "mkdocs.yml"

    logger.info("Generating Terraform docs")
    logger.info("Reading MkDocs config from: {}", str(mkdocs_config_path))

    # Load the config file
    with mkdocs_config_path.open() as file:
        mkdocs_config = yaml.safe_load(file)

    # Read all the file paths from the `nav` object
    nav_items: list[str] = get_nav_item_paths(mkdocs_config.get("nav", []))

    for file_path in nav_items:
        generate_docs_for_project(repo_root_dir, Path(file_path))


if __name__ == "__main__":
    generate_terraform_docs()
