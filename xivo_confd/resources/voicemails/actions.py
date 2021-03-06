# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


import logging

from flask.globals import request
from flask.blueprints import Blueprint
from flask.helpers import make_response, url_for

from xivo_confd import config
from xivo_confd.helpers.route_generator import RouteGenerator
from xivo_confd.helpers.formatter import Formatter
from xivo_confd.resources.voicemails import mapper
from xivo_confd.helpers import serializer
from xivo_confd.helpers.common import extract_search_parameters
from xivo_dao.data_handler.voicemail.model import Voicemail
from xivo_dao.data_handler.voicemail import services as voicemail_services

from xivo_confd.flask_http_server import content_parser
from xivo_confd.helpers.mooltiparse import Field, Unicode, Int, Boolean


logger = logging.getLogger(__name__)
blueprint = Blueprint('voicemails', __name__, url_prefix='/%s/voicemails' % config.VERSION_1_1)
route = RouteGenerator(blueprint)
formatter = Formatter(mapper, serializer, Voicemail)

document = content_parser.document(
    Field('id', Int()),
    Field('name', Unicode()),
    Field('number', Unicode()),
    Field('context', Unicode()),
    Field('password', Unicode()),
    Field('email', Unicode()),
    Field('language', Unicode()),
    Field('timezone', Unicode()),
    Field('max_messages', Int()),
    Field('attach_audio', Boolean()),
    Field('delete_messages', Boolean()),
    Field('ask_password', Boolean())
)


@route('')
def list():
    search_parameters = extract_search_parameters(request.args)
    search_result = voicemail_services.search(**search_parameters)
    result = formatter.list_to_api(search_result.items, search_result.total)
    return make_response(result, 200)


@route('/<int:voicemailid>')
def get(voicemailid):
    voicemail = voicemail_services.get(voicemailid)
    result = formatter.to_api(voicemail)
    return make_response(result, 200)


@route('', methods=['POST'])
def create():
    data = document.parse(request)
    voicemail = formatter.dict_to_model(data)
    voicemail = voicemail_services.create(voicemail)
    result = formatter.to_api(voicemail)
    location = url_for('.get', voicemailid=voicemail.id)
    return make_response(result, 201, {'Location': location})


@route('/<int:voicemailid>', methods=['PUT'])
def edit(voicemailid):
    data = document.parse(request)
    voicemail = voicemail_services.get(voicemailid)
    formatter.update_dict_model(data, voicemail)
    voicemail_services.edit(voicemail)
    return make_response('', 204)


@route('/<int:voicemailid>', methods=['DELETE'])
def delete(voicemailid):
    voicemail = voicemail_services.get(voicemailid)
    voicemail_services.delete(voicemail)
    return make_response('', 204)
