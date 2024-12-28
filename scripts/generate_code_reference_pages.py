#!/usr/bin/env python3

"""Generate Python code reference pages.

Based on: https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages
"""

# Standard Libraries
from pathlib import Path

# Third-party Libraries
import mkdocs_gen_files
import yaml
from loguru import logger
from mkdocs_gen_files.nav import Nav

# The sub-directory where code reference files will be generated
CODE_REFERENCE_DIR_NAME: str = "reference"


def get_code_dir_paths(repo_root_dir: Path) -> list[str]:
    """Parse code directories from `mkdocstrings` config.

    Args:
        repo_root_dir (Path): The root directory of the repo where the `mkdocs.yml` config is stored

    Returns:
        list[str]: A list of paths containing code to generate reference pages for (relative to the repo root directory)
    """
    mkdocs_config_path: Path = repo_root_dir / "mkdocs.yml"

    logger.info("Loading MkDocs config from: {}", str(mkdocs_config_path))

    with mkdocs_config_path.open() as file:
        mkdocs_config = yaml.safe_load(file)

    paths: list[str] = []

    # Load code paths from the `mkdocstrings` plugin config, if it exists
    if plugins := [p for p in mkdocs_config.get("plugins") if "mkdocstrings" in p]:
        paths = plugins[0].get("mkdocstrings").get("handlers", {}).get("python", {}).get("paths") or []

    if not plugins:
        logger.warning("No code paths found in `mkdocstrings` config; defaulting to the project root")
        paths.append(str(repo_root_dir))

    return paths


def generate_code_reference_pages(python_src_dir: Path) -> None:
    """Recursively find and generate reference pages for Python source files.

    Args:
        python_src_dir (Path): A directory containing Python source files
    """
    logger.info("Generating code reference for '{}'", python_src_dir)

    nav: Nav = Nav()

    # Recursively iterate over all Python files
    for path in sorted(python_src_dir.rglob("*.py")):
        module_path: Path = path.relative_to(python_src_dir).with_suffix("")
        doc_path: Path = Path(f"{module_path}.md")
        full_doc_path: Path = Path(CODE_REFERENCE_DIR_NAME) / doc_path

        parts = tuple(module_path.parts)

        # Skip `__main__.py` and create `index.md` in place of `__init__.py` files
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        elif parts[-1] == "__main__":
            continue

        # Add the page to the navigation
        nav[parts] = doc_path.as_posix()

        # Generate code reference files using `mkdocstrings` autodoc syntax
        # Note: Parent directories will be generated automatically
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            identifier: str = ".".join(parts)
            print("::: " + identifier, file=fd)

        mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(repo_root_dir))

    # Write the navigation data to the file specified by the `nav_file` setting for `literate-nav`
    with mkdocs_gen_files.open(f"{CODE_REFERENCE_DIR_NAME}/NAV.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


if __name__ == "__main__":
    repo_root_dir: Path = Path(__file__).parent.parent

    for path in get_code_dir_paths(repo_root_dir):
        generate_code_reference_pages(repo_root_dir / path)
