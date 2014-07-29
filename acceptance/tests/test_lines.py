from test_api import scenarios as s
from test_api.helpers.line import generate_line


REQUIRED = ['context', 'device_slot']

BOGUS = [('context', 123, 'unicode string'),
         ('device_slot', '1', 'integer')]


class TestLineResource(s.GetScenarios, s.CreateScenarios, s.EditScenarios, s.DeleteScenarios):

    url = "/lines_sip"
    resource = "Line"
    required = REQUIRED
    bogus_fields = BOGUS

    def create_resource(self):
        line = generate_line()
        return line['id']
