# AGENTS.md - Coding Guidelines

## Build & Serve Commands

- **Build**: `make html` - Generates static HTML from markdown content
- **Development Server**: `make serve` - Runs local HTTP server on port 8000
- **Regenerate**: `make regenerate` - Watches for changes and rebuilds
- **Publish**: `make publish` - Builds and deploys to GitHub Pages
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
- `Makefile` - Build automation tasks

## Code Style & Conventions

**Python**:
- Python 3 with UTF-8 encoding (`#!/usr/bin/env python`, `# -*- coding: utf-8 -*-`)
- Makefile for build automation

**Markdown Content**:
- Default metadata: `status: draft` (use `published` or `unpublished`)
- Filenames follow standard markdown convention
- Configuration via YAML front matter

**Configuration**:
- Environment variable: `SITEURL` (defaults to `http://localhost:8000`)
- No linting/testing framework - content-driven site
- Git workflow: develop on main, deploy to `gh-pages` branch
