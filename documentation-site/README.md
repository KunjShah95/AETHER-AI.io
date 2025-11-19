# NEXUS AI Documentation Site

This directory contains the source code for the NEXUS AI documentation site, built with [MkDocs](https://www.mkdocs.org/).

## Structure

- `mkdocs.yml`: Configuration file.
- `docs/`: Markdown source files.

## Running Locally

1.  **Install MkDocs and Material Theme**:
    ```bash
    pip install mkdocs mkdocs-material
    ```

2.  **Serve the site**:
    ```bash
    mkdocs serve
    ```
    Open `http://127.0.0.1:8000` in your browser.

3.  **Build the site**:
    ```bash
    mkdocs build
    ```
    The static site will be generated in the `site/` directory.
