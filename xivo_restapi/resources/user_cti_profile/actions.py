# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Avencall
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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from xivo_restapi.resources.users.routes import route
from xivo_restapi.resources.user_cti_profile.formatter import UserCtiProfileFormatter
from flask.globals import request
from xivo_dao.data_handler.user_cti_profile import services as user_cti_profile_services
from flask.helpers import make_response

formatter = UserCtiProfileFormatter()


@route('/<int:userid>/cti', methods=['PUT'])
def edit_cti_configuration(userid):
    data = request.data.decode("utf-8")
    model = user_cti_profile_services.get_by_user_id(userid)
    formatter.update_model(model, data)
    user_cti_profile_services.edit(model)
    return make_response('', 204)


@route('/<int:userid>/cti', methods=['GET'])
def get_cti_configuration(userid):
    model = user_cti_profile_services.get_by_user_id(userid)
    result = formatter.to_api(model)
    return make_response(result, 200)
