from test_api import scenarios as s
from test_api import helpers


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
        extension = helpers.extension.generate_extension()
        return "/extensions/{}".format(extension['id'])
