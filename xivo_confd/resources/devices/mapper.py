# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from flask.helpers import url_for

# mapping = {model_field: api_field}
MAPPING = {
    'id': 'id',
    'ip': 'ip',
    'mac': 'mac',
    'sn': 'sn',
    'plugin': 'plugin',
    'template_id': 'template_id',
    'model': 'model',
    'vendor': 'vendor',
    'version': 'version',
    'status': 'status',
    'description': 'description',
    'options': 'options',
}


def add_links_to_dict(device_dict, device):
    device_location = url_for('.get', deviceid=device.id, _external=True)
    device_dict.update({
        'links': [
            {
                'rel': 'devices',
                'href': device_location
            }
        ]
    })
