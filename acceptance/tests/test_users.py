from test_api import scenarios as s
from test_api import assertions as a
from test_api.helpers.user import generate_user
from test_api import restapi

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
        user = generate_user()
        url = restapi.users(user['id'])
        return str(url)

    def test_invalid_mobile_phone_number(self):
        response = restapi.users.post(firstname='firstname',
                                      mobile_phone_number='ai67cba74cba6kw4acwbc6w7')
        a.assert_invalid_parameter(response, 'mobile_phone_number')
