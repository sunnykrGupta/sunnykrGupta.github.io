# sunnykrGupta.github.io
Personal Blog about random Computer Science work.

### Fresh Start in new workstation
```
pip install pelican markdown

#share_post plugin requires BeautifulSoup
pip install beautifulsoup4

#Install Fabric and use it to build and serve the site locally:
pip install fabric
```

#### Clone plugins for use
```
git clone https://github.com/getpelican/pelican-plugins
```

#### Dependency:
https://cryptography.io/en/latest/installation/


> Notes for deploying on github-pages
```
pip install ghp-import
```

## Run locally, before that change SITEURL to proper domain.
```
pkill -f SimpleHTTPServer | fab build && fab serve
```

# Run to publish changes, before that change SITEURL to proper domain.
```
fab publish
```

