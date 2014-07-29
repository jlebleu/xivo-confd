import re
import unittest

from test_api import scenarios as s
from test_api import helpers as h
from test_api import assertions as a
from test_api import restapi
from test_api import fixtures

from test_api.helpers.user_line import user_and_line_associated

no_line_error = re.compile(r"user with id \d+ does not have any line")
already_associated_error = re.compile(r"user with id \d+ already has a voicemail")
no_voicemail_error = re.compile(r"User with id=\d+ does not have a voicemail")


class TestUserVoicemailAssociation(s.AssociationScenarios,
                                   s.DissociationScenarios,
                                   s.AssociationGetScenarios):

    left_resource = "User"
    right_resource = "Line"
    left_field = "user"
    right_field = "voicemail"
    associated_error = re.compile("user with id \d+ already has a voicemail")
    not_associated_error = re.compile("error")

    def create_resources(self):
        self.user_id = h.user.generate_user()['id']
        self.line_id = h.line.generate_line()['id']
        h.user_line.associate(self.user_id, self.line_id)

        self.voicemail_id = h.voicemail.generate_voicemail()['id']
        return self.user_id, self.voicemail_id

    def delete_resources(self, user_id, voicemail_id):
        h.voicemail.delete_voicemail(self.voicemail_id)

        h.user_line.dissociate(self.user_id, self.line_id)
        h.user.delete_user(self.user_id)
        h.voicemail.delete_voicemail(self.voicemail_id)

    def associate_resources(self, user_id, voicemail_id):
        return restapi.users(user_id).voicemail.post(voicemail_id=voicemail_id)

    def dissociate_resources(self, user_id, voicemail_id):
        return restapi.users(user_id).voicemail.delete()

    def get_association(self, user_id, voicemail_id):
        return restapi.users(user_id).voicemail.get()

    @unittest.skip("fix status code")
    def test_dissociation_when_left_does_not_exist(self):
        pass

    @unittest.skip("fix status code")
    def test_dissociation_when_right_does_not_exist(self):
        pass

    @unittest.skip("fix error message")
    def test_dissociation_when_not_associated(self):
        pass


@fixtures.user()
@fixtures.voicemail()
def test_associate_when_user_has_no_line(user, voicemail):
    response = restapi.users(user['id']).voicemail.post(voicemail_id=voicemail['id'])
    a.assert_error(response, no_line_error, 400)


@fixtures.user()
@fixtures.line()
@fixtures.voicemail()
def test_associate_when_already_associated(user, line, voicemail):
    with user_and_line_associated(user, line):
        response = restapi.users(user['id']).voicemail.post(voicemail_id=voicemail['id'])
        response.assert_ok()

        response = restapi.users(user['id']).voicemail.post(voicemail_id=voicemail['id'])
        a.assert_error(response, already_associated_error)


@fixtures.user()
def test_get_when_not_associated(user):
    response = restapi.users(user['id']).voicemail.get()
    a.assert_error(response, no_voicemail_error)
