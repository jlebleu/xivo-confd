# -*- coding: utf-8 -*-

# Copyright (C) 2012-2013 Avencall
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

from mock import Mock
from xivo_dao import voicemail_dao
from xivo_dao.alchemy.voicemail import Voicemail
from xivo_restapi.services.utils.exceptions import NoSuchElementException
from xivo_restapi.services.voicemail_management import VoicemailManagement
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.voicemail_manager = VoicemailManagement()

    def test_get_all_users(self):
        voicemail1 = Voicemail()
        voicemail1.mailbox = "123"
        voicemail2 = Voicemail()
        voicemail2.mailbox = "456"
        expected_result = [voicemail1, voicemail2]
        voicemail_dao.all = Mock()
        voicemail_dao.all.return_value = expected_result

        result = self.voicemail_manager.get_all_voicemails()
        self.assertEquals(result, expected_result)
        voicemail_dao.all.assert_called_once_with() #@UndefinedVariable

    def test_update_voicemail(self):
        voicemailid = 1
        voicemail_dao.update = Mock()
        voicemail_dao.get = Mock()
        voicemail_dao.get.return_value = Voicemail()
        data = {"mailbox": "123",
                "fullname": "test"}
        self.voicemail_manager.edit_voicemail(voicemailid, data)
        voicemail_dao.get.assert_called_with(1) #@UndefinedVariable
        voicemail_dao.update.assert_called_with(voicemailid, data) #@UndefinedVariable

    def test_update_unexisting_voicemail(self):
        voicemailid = 1
        voicemail_dao.update = Mock()
        voicemail_dao.get = Mock()
        voicemail_dao.get.return_value = None
        data = {"mailbox": "123",
                "fullname": "test"}
        self.assertRaises(NoSuchElementException, self.voicemail_manager.edit_voicemail, voicemailid, data)
        voicemail_dao.get.assert_called_with(1) #@UndefinedVariable
