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

from flask import Flask
from rest_http_server import api
from flask import Blueprint
from tests.test_config import TestConfig

app = Flask(__name__)
main = Blueprint("main", __name__)

app.register_blueprint(api)
app.register_blueprint(main)

class FlaskHttpServer(object):

    def run(self):
        app.run(host=TestConfig.XIVO_RECORD_SERVICE_ADDRESS, port=TestConfig.XIVO_RECORD_SERVICE_PORT, debug=True)



@app.route("/")
def root():
    return "XiVO REST server"
