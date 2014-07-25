from test_api import scenarios as s
from test_api import assertions as a
from test_api.helpers import user as user_helper
from test_api import client

FIELDS = ['firstname',
          'lastname',
          'timezone',
          'language',
          'description',
          'caller_id',
          'outgoing_caller_id',
          'mobile_phone_number',
          'username',
          'password',
          'music_on_hold',
          'preprocess_subroutine',
          'userfield']

REQUIRED = ['firstname']

BOGUS = [(f, 123, 'unicode string') for f in FIELDS]


class TestUserResource(s.GetScenarios, s.CreateScenarios, s.EditScenarios, s.DeleteScenarios):

    url = "/users"
    resource = "User"
    required = REQUIRED
    bogus_fields = BOGUS

    def create_url(self):
        user = user_helper.add_user(firstname='firstname')
        return "/users/{}".format(user['id'])

    def test_invalid_mobile_phone_number(self):
        data = {'firstname': 'firstname',
                'mobile_phone_number': 'ao8as7ncia7s6encai7se6cb'}

        response = client.post(self.url, data)
        a.assert_invalid_parameter(response, 'mobile_phone_number')
