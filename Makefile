PY=python3
PELICAN=$(VENV)/bin/pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py
VENV=$(BASEDIR)/venv

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

.PHONY: help venv install html clean regenerate serve publish github

help:
	@echo 'Makefile for a pelican Web site'
	@echo ''
	@echo 'Usage:'
	@echo '   make venv                        create a Python virtual environment'
	@echo '   make install                     install dependencies in venv'
	@echo '   make html                        (re)generate the web site'
	@echo '   make clean                       remove the generated files'
	@echo '   make regenerate                  regenerate files upon modification'
	@echo '   make publish                     generate using production settings'
	@echo '   make serve [PORT=8000]           serve site at http://localhost:8000'
	@echo '   make github                      upload the web site via gh-pages'
	@echo ''
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html'
	@echo ''

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(VENV)/bin/pip install --upgrade pip setuptools wheel
	$(VENV)/bin/pip install -r requirements.txt

html: $(VENV)
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve: html
ifdef PORT
	cd $(OUTPUTDIR) && $(VENV)/bin/python -m http.server $(PORT)
else
	cd $(OUTPUTDIR) && $(VENV)/bin/python -m http.server
endif

github: publish
	ghp-import $(OUTPUTDIR)
	git push origin gh-pages

publish:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

# devserver:
# ifdef PORT
# 	$(BASEDIR)/develop_server.sh restart $(PORT)
# else
# 	$(BASEDIR)/develop_server.sh restart
# endif

# stopserver:
# 	kill -9 `cat pelican.pid`
# 	kill -9 `cat srv.pid`
# 	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'
