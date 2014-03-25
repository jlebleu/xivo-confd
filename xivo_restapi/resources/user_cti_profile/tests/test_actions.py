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
from hamcrest import assert_that, equal_to

from mock import patch
from xivo_restapi.helpers.tests.test_resources import TestResources
from xivo_dao.data_handler.user_cti_profile.model import UserCtiProfile
from xivo_dao.data_handler.exception import ElementNotExistsError

BASE_URL = "/1.1/users/%s/cti"


class TestUserVoicemailActions(TestResources):

    @patch('xivo_dao.data_handler.user_cti_profile.services.edit')
    def test_update_cti_configuration(self, user_cti_profile_edit):
        user_id = 1
        cti_profile_id = 2

        expected_status_code = 204

        data = {
            'cti_profile_id': cti_profile_id,
            'enabled': True
        }
        data_serialized = self._serialize_encode(data)

        result = self.app.put(BASE_URL % user_id, data=data_serialized)

        assert_that(result.status_code, equal_to(expected_status_code))

    @patch('xivo_dao.data_handler.user_cti_profile.services.get_by_user_id')
    def test_get_cti_configuration(self, get_by_user_id):
        user_id = 1
        cti_profile_id = 2

        expected_status_code = 200
        expected_result = {
            "user_id": user_id,
            "cti_profile_id": cti_profile_id,
            "enabled": True,
            "links": [
                {
                    "rel": "users",
                    "href": "http://localhost/1.1/users/%s" % user_id
                },
                {
                    "rel": "cti_profiles",
                    "href": "http://localhost/1.1/cti_profiles/%s" % cti_profile_id
                }
            ]
        }

        user_cti_profile = UserCtiProfile(user_id=user_id, cti_profile_id=cti_profile_id, enabled=True)
        get_by_user_id.return_value = user_cti_profile

        result = self.app.get(BASE_URL % user_id)

        assert_that(result.status_code, equal_to(expected_status_code))
        assert_that(self._serialize_decode(result.data), equal_to(expected_result))

    @patch('xivo_dao.data_handler.user_cti_profile.services.get_by_user_id')
    def test_get_cti_profile_association_not_exists(self, get_by_user_id):
        user_id = 1

        expected_status_code = 200
        expected_result = {
            "user_id": user_id,
            "cti_profile_id": None,
            "enabled": False,
            "links": [
                {
                    "rel": "users",
                    "href": "http://localhost/1.1/users/%s" % user_id
                }
            ]
        }

        user_cti_profile = UserCtiProfile(user_id=user_id, cti_profile_id=None, enabled=False)
        get_by_user_id.return_value = user_cti_profile

        result = self.app.get(BASE_URL % user_id)

        assert_that(result.status_code, equal_to(expected_status_code))
        assert_that(self._serialize_decode(result.data), equal_to(expected_result))

    @patch('xivo_dao.data_handler.user_cti_profile.services.get_by_user_id')
    def test_get_cti_profile_association_unexisting_user(self, get_by_user_id):
        user_id = 1

        expected_status_code = 404
        expected_result = ['user with id=%d does not exist' % user_id]

        get_by_user_id.side_effect = ElementNotExistsError('user', id=user_id)

        result = self.app.get(BASE_URL % user_id)

        assert_that(result.status_code, equal_to(expected_status_code))
        assert_that(self._serialize_decode(result.data), equal_to(expected_result))
