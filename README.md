# Documentation Builder

This project collects and integrates a variety of tools for automatically generating and building project documentation.

It uses:

- [`terraform-docs`](https://terraform-docs.io/) to generate documentation for Terraform projects and modules
- [`inframap`](https://github.com/cycloidio/inframap) to generate diagrams of planned and deployed cloud infrastructure
- [`draw.io`](https://www.drawio.com/) for manual diagramming
- [`mkdocstrings`](https://mkdocstrings.github.io/) to generate Python code documentation
- [`mkdocs`](https://www.mkdocs.org/) to collect and build it all into static web pages

---

## Quickstart

> [!TIP]
> Sample data, including a Python package, draw.io diagram, and Terraform configs, have been provided for demonstration
> purposes

1. Install Docker and Docker Compose
2. Clone the repo
3. Run `docker compose up server`
4. Navigate to [`http://localhost:8000`](http://localhost:8000) in your browser to view the sample project docs

---

## Usage

> [!WARNING]
> The `docs/reference` directory is reserved for `mkdocstrings`; any files created here may be overwritten!
>
> To change the name of this directory, modify the `CODE_REFERENCE_DIR_NAME` constant in
> `scripts/generate_code_reference_pages.py` and update the associated `nav` element entry in `mkdocs.yml`.

1. Remove the sample data from the `docs`, `src`, and `terraform` directories
2. Add Terraform projects to the `terraform` sub-directory and modules to the `terraform/modules` sub-directory
3. Update the `nav` element in `mkdocs.yml` to reference your desired Terraform projects and modules
    - This affords greater control over how (and which) projects and modules are listed
4. Add Python packages to the `src` sub-directory
    - To use a directory other than `src`, simply modify the `paths` settings under the `mkdocstrings` plugin in `mkdocs.yml`
5. Add any [`draw.io`](https://www.drawio.com/) diagrams to `docs/assets/diagrams`
6. Add images to `docs/assets/images`
7. Add Markdown files to the `docs` sub-directory

    - Image: `![<IMAGE_TITLE>](assets/images/<IMAGE_NAME>.<EXT>)`
        - Diagrams created by `inframap` are named for their project path, with underscores replacing directory separators (e.g., `terraform/load_balancer` becomes `terraform_load_balancer.png`)
    - Multi-page `draw.io` diagrams: `![](assets/diagrams/<FILE_NAME>.drawio)`
    - Single page from a multi-page `draw.io` diagram: `![<PAGE_NAME>](assets/diagrams/<FILE_NAME>.drawio)`

8. Run the documentation builder

    ```bash
    # Serve documentation on port 8000 with live-reload (runs in the foreground)
    docker compose up server

    # Build documentation to the `site` sub-directory
    docker compose run --rm builder
    ```
