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


from xivo_dao.data_handler.user_cti_profile.model import UserCtiProfile
from xivo_confd.helpers import serializer

from xivo_confd.helpers.formatter import Formatter
from xivo_confd.resources.user_cti_profile import mapper


class UserCtiProfileFormatter(Formatter):

    def __init__(self):
        Formatter.__init__(self, mapper, serializer, UserCtiProfile)

    def dict_to_model(self, data, user_id):
        model = Formatter.dict_to_model(self, data)
        model.user_id = user_id
        return model
