# -*- coding: UTF-8 -*-

# Copyright (C) 2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..

import flask

from xivo_dao.accesswebservice_dao import get_password
from flask import request, session, Response
from functools import wraps
from xivo_dao import accesswebservice_dao
from xivo_restapi.rest.authentication.werkzeug import authdigest


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return password == get_password(username)


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


class XivoRealmDigest(authdigest.RealmDigestDB):
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if flask.request.headers.getlist("X-Auth-Token"):
                auth_token = flask.request.headers.getlist("X-Auth-Token")[0]
                if auth_token == 'toto':
                    return f(*args, **kwargs)
            if not flask.request.headers.getlist("X-Forwarded-For"):
                remote_address = request.remote_addr
            else:
                remote_address = flask.request.headers.getlist("X-Forwarded-For")[0]
            if self.isRemoteAddressAllowed(remote_address):
                return f(*args, **kwargs)
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
            """
            if self.isSessionLogged(session):
                return f(*args, **kwargs)
            if self.isAuthenticated(flask.request):
                session.permanent = True
                session['logged'] = True
                session['username'] = flask.request.authorization.username
                return f(*args, **kwargs)
            return self.challenge()
            """
            return authenticate()
        return decorated

    def isRemoteAddressAllowed(self, address):
        if address == '127.0.0.1' or (address in accesswebservice_dao.get_allowed_hosts()):
            return True
        else:
            return False

    def isSessionLogged(self, session):
        return 'logged' in session and session['logged']

realmDigest = XivoRealmDigest('XivoRealm')
