from test_api import scenarios as s
from test_api import client


REQUIRED = ['exten', 'context']

BOGUS = [('exten', 123, 'unicode string'),
         ('context', 123, 'unicode string'),
         ('commented', 'true', 'boolean')]


class TestExtensionResource(s.GetScenarios, s.CreateScenarios, s.EditScenarios, s.DeleteScenarios):

    url = "/extensions"
    resource = "Extension"
    required = REQUIRED
    bogus_fields = BOGUS

    def create_url(self):
        response = client.post("/extensions", {'context': 'default', 'exten': '1444'})
        response.assert_status(201)
        return "/extensions/{}".format(response.json['id'])
