#!/usr/bin/env python2

from bottle import route, run, template, default_app
import subprocess
import requests
import logging
import socket
import yaml
import os

application = default_app()

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

IP_ADDR = socket.gethostbyaddr('localhost')[2][0]
GIT_REPLICATION_MAP = '/usr/local/www/apache24/hooks/replication.map'


def _subprocess(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]


def _config(key):
    try:
        with open(GIT_REPLICATION_MAP) as fh_:
            config = yaml.safe_load(fh_)
            return config.get(key)
    except IOError as exc:
        LOG.debug('Unable to load replication.map')


def _clone(project, repo):
    GIT = _config('git_path')
    PATH = _config('repo_path')
    MAP = _config('map')
    try:
        SOURCE = MAP[IP_ADDR]['source']
    except KeyError as exc:
        SOURCE = _config('default_source')
    LOG.debug(GIT)
    LOG.debug(PATH)
    LOG.debug(SOURCE)


    if not os.path.exists(os.path.join(PATH, project, repo)):
        os.chdir(PATH)
        cmd = '{0} clone --bare {1}/{2}/{3} {2}/{3}'.format(GIT, SOURCE, project, repo)
        LOG.debug(cmd)
        return _subprocess(cmd)
    return _fetch(project, repo)


def _fetch(project, repo):
    GIT = _config('git_path')
    PATH = _config('repo_path')

    if os.path.exists(os.path.join(PATH ,project ,repo)):
        os.chdir(os.path.join(PATH, project, repo))
        cmd = '{0} fetch'.format(GIT)
        LOG.debug(cmd)
        return _subprocess(cmd)
    return _clone(project, repo)


def _notify(project, repo):
    MAP = _config('map')
    if MAP[IP_ADDR]['notify']:
        for server in MAP[IP_ADDR]['notify']:
            url = 'http://' + server + ':8888/clone/' + project + '/' + repo
            LOG.debug(url)
            requests.get(url)
    else:
        LOG.debug('Not notifying any peers')


@route('/clone/<project>/<repo>')
def clone(project, repo):
    _clone(project,repo)
    _notify(project, repo)


@route('/fetch/<project>/<repo>')
def pull(project, repo):
    _fetch(project, repo)
    _notify(project, repo)

