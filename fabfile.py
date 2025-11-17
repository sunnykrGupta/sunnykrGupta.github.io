import os

import fabric.contrib.project as project
from fabric.api import *
from pelicanconf import SITEURL

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    local('pelican -s pelicanconf.py')

def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def rebuild():
    clean()
    build()
    serve()

def regenerate():
    local('pelican -r -s pelicanconf.py')

def preview():
    local('pelican -s publishconf.py')

def showpid():
    local('lsof -i :8000')

def killserver():
    local('pkill -9 -f SimpleHTTPServer')


@hosts(production)
def publish():
    if 'localhost' not in SITEURL:
        local('pelican content -o output -s pelicanconf.py')
        local('ghp-import output')
        print("Pushing changes to Github pages")
        local('git push origin gh-pages:master')
    else:
        print("Publish Aborted !! \n")
        print("Correct SITEURL : ", SITEURL)
