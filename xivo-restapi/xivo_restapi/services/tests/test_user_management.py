'''
Created on Feb 20, 2013

@author: jean
'''
from mock import Mock
from xivo_dao import user_dao
from xivo_dao.alchemy.userfeatures import UserFeatures
from xivo_restapi.services.user_management import UserManagement
from xivo_restapi.services.utils.exceptions import NoSuchElementException
import copy
import unittest


class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self._userManager = UserManagement()

    def test_get_all_users(self):
        user1 = UserFeatures()
        user1.firstname = 'test1'
        user2 = UserFeatures()
        user2.firstname = 'test2'
        user_dao.get_all = Mock()
        user_dao.get_all.return_value = [user1, user2]
        result = self._userManager.get_all_users()
        user_dao.get_all.assert_any_call()
        self.assertEqual(result, [user1, user2])

    def test_get_user(self):
        user1 = UserFeatures()
        user1.firstname = 'test1'
        user_dao.get = Mock()
        user_dao.get.return_value = user1
        result = self._userManager.get_user(1)
        user_dao.get.assert_called_with(1)
        self.assertEqual(result, user1)

    def test_get_non_existing_user(self):
        def mock_get(userid):
            raise LookupError()

        user_dao.get = Mock()
        user_dao.get.side_effect = mock_get
        self.assertRaises(NoSuchElementException, self._userManager.get_user, 1)
        user_dao.get.assert_called_with(1)
        user_dao.get.side_effect = None

    def test_create_user(self):
        user1 = UserFeatures()
        user1.firstname = 'test1'
        user_dao.add_user = Mock()
        self._userManager.create_user(user1)
        user_dao.add_user.assert_called_with(user1)
        self.assertEqual(user1.description, '')

    def test_edit_user(self):
        data = {'id': 2,
                'lastname': 'test',
                'non_existing_column': 'value'}
        data_copy = copy.deepcopy(data)
        user_dao.update = Mock()
        user_dao.update.return_value = 1
        self._userManager.edit_user(1, data)
        del data_copy['id']
        del data_copy['non_existing_column']
        user_dao.update.assert_called_once_with(1, data_copy)

    def test_edit_user_not_found(self):
        data = {'lastname': 'test'}
        user_dao.update = Mock()
        user_dao.update.return_value = 0
        self.assertRaises(NoSuchElementException, self._userManager.edit_user,
                          1, data)

    def test_delete_user(self):
        user_dao.delete = Mock()
        user_dao.delete.return_value = 1
        self._userManager.delete_user(1)
        user_dao.delete.assert_called_with(1)

    def test_delete_unexisting_user(self):
        user_dao.delete = Mock()
        user_dao.delete.return_value = 0
        self.assertRaises(NoSuchElementException, self._userManager.delete_user, 1)
        user_dao.delete.assert_called_with(1)