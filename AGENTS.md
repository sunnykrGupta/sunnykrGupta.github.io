# AGENTS.md - Coding Guidelines

## Build & Serve Commands

- **Build**: `make html` or `fab build` - Generates static HTML from markdown content
- **Development Server**: `make devserver` or `fab serve` - Runs local HTTP server on port 8000
- **Regenerate**: `make regenerate` or `fab regenerate` - Watches for changes and rebuilds
- **Publish**: `make publish` or `fab publish` - Builds and deploys to GitHub Pages
- **Clean**: `make clean` - Removes generated output directory

## Architecture & Structure

**Pelican Static Site Generator** - Converts markdown articles to HTML blog
- `content/articles/` - Blog post markdown files (default status: draft)
- `content/pages/` - Static page content
- `content/images/` - Static assets
- `output/` - Generated HTML (gitignored)
- `pelican-svbhack-responsive/` - Custom theme
- `pelicanconf.py` - Development config (localhost:8000)
- `publishconf.py` - Production config
- `fabfile.py` - Fabric deployment tasks

## Code Style & Conventions

**Python**:
- Python 3 with UTF-8 encoding (`#!/usr/bin/env python`, `# -*- coding: utf-8 -*-`)
- Fabric tasks for common operations
- Import conventions: `from fabric.api import *`

**Markdown Content**:
- Default metadata: `status: draft` (use `published` or `unpublished`)
- Filenames follow standard markdown convention
- Configuration via YAML front matter

**Configuration**:
- Environment variable: `SITEURL` (defaults to `http://localhost:8000`)
- No linting/testing framework - content-driven site
- Git workflow: develop on main, deploy to `gh-pages` branch
