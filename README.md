# sunnykrGupta.github.io

A personal blog about Computer Science topics, built with Pelican and hosted on GitHub Pages.

### Pelican Theme

The theme is maintained in a separate repository:
- **Repository**: https://github.com/sunnykrGupta/pelican-svbhack-responsive
- **Based on**: [svbtle responsive design patterns](https://github.com/gfidente/pelican-svbhack)
- **License**: MIT

## Overview

This is a static site generator setup using Pelican that converts markdown articles into a static HTML blog. The site is deployed to GitHub Pages via the `gh-pages` branch.

## Quick Start

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sunnykrGupta/sunnykrGupta.github.io.git
cd sunnykrGupta.github.io
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Building and Running

- **Build static HTML**: `make html`
- **Run local server**: `make serve` (runs on http://localhost:8000)
- **Build and serve**: `make html && make serve`
- **Watch for changes and rebuild**: `make regenerate`
- **Build for production**: `make publish`
- **Deploy to GitHub Pages**: `make github`
- **Clean output**: `make clean`

For more build commands, run `make help`.

## Project Structure

```
.
├── content/
│   ├── articles/       # Blog post markdown files
│   ├── pages/          # Static page content
│   └── images/         # Static assets
├── output/             # Generated HTML (gitignored)
├── pelican-svbhack-responsive/  # Custom responsive theme
├── pelicanconf.py      # Development config
├── publishconf.py      # Production config
├── Makefile            # Build automation
└── requirements.txt    # Python dependencies
```

## Configuration

- **Development**: Uses `pelicanconf.py` with `SITEURL = 'http://localhost:8000'`
- **Production**: Uses `publishconf.py` with proper domain URL
- **Blog posts**: Stored in `content/articles/` with default status `draft`
  - Use `status: published` in frontmatter to publish

## Creating Posts

Create a new markdown file in `content/articles/` with YAML frontmatter:

```markdown
Title: Your Post Title
Date: 2024-11-17
Author: Your Name
Status: draft

Your content here...
```

## Deploying (GitHub Pages) using Github Actions

[Deploy blog to GitHub Pages - .github/workflows](./github/workflows/deploy-pages.yml)

## Notes

- The `venv/` directory is created locally and not committed
- For custom plugins, clone from: https://github.com/getpelican/pelican-plugins
