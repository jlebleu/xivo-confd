import re
import unittest

from test_api.scenarios import AssociationScenarios, DissociationScenarios, AssociationGetScenarios
from test_api import helpers
from test_api import restapi
from test_api import assertions as a
from test_api import fixtures

from contextlib import contextmanager


FAKE_ID = 999999999


class TestUserLineAssociation(AssociationScenarios, DissociationScenarios, AssociationGetScenarios):

    left_resource = "User"
    right_resource = "Line"
    left_field = 'user_id'
    right_field = 'line_id'
    associated_error = re.compile(r"user is already associated to this line")
    not_associated_error = re.compile(r"user is not associated")

    def create_resources(self):
        user = helpers.user.generate_user()
        line = helpers.line.generate_line()
        return user['id'], line['id']

    def delete_resources(self, user_id, line_id):
        helpers.user.delete_user(user_id)
        helpers.line.delete_line(line_id)

    def associate_resources(self, user_id, line_id):
        return restapi.users(user_id).lines.post(line_id=line_id)

    def dissociate_resources(self, user_id, line_id):
        return restapi.users(user_id).lines(line_id).delete()

    def get_association(self, user_id, line_id):
        return restapi.users(user_id).lines.get()

    @unittest.skip("will be fixed after refactoring DAO exceptions")
    def test_dissociation_when_left_does_not_exist(self):
        pass

    @unittest.skip("will be fixed after refactoring DAO exceptions")
    def test_dissociation_when_not_associated(self):
        pass

    @unittest.skip("will be fixed after refactoring DAO exceptions")
    def test_dissociation_when_right_does_not_exist(self):
        pass


@contextmanager
def user_and_line_associated(user, line):
    response = restapi.users(user['id']).lines.post(line_id=line['id'])
    response.assert_status(201)

    yield

    restapi.users(user['id']).lines(line['id']).delete()


@fixtures.user()
@fixtures.line()
def test_associate_when_user_already_associated_to_same_line(user, line):
    with user_and_line_associated(user, line):
        response = restapi.users(user['id']).lines.post(line_id=line['id'])
        a.assert_invalid_parameter(response, 'user is already associated to this line')


@fixtures.user()
@fixtures.line()
@fixtures.line()
def test_associate_when_user_already_associated_to_another_line(user, first_line, second_line):
    with user_and_line_associated(user, first_line):
        response = restapi.users(user['id']).lines.post(line_id=first_line['id'])
        a.assert_invalid_parameter(response, 'user is already associated to this line')


@fixtures.user()
@fixtures.user()
@fixtures.line()
def test_dissociate_second_user_before_first(first_user, second_user, line):
    with user_and_line_associated(first_user, line), user_and_line_associated(second_user, line):
        response = restapi.users(first_user['id']).lines(line['id']).delete()
        a.assert_invalid_parameter(response, 'There are secondary users associated to this line')


@fixtures.user()
@fixtures.line()
def test_delete_user_when_user_and_line_associated(user, line):
    with user_and_line_associated(user, line):
        response = restapi.users(user['id']).delete()
        a.assert_delete_error(response, 'User', 'user still associated to a line')
