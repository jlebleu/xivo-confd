from test_api import scenarios as s
from test_api.helpers import line as line_helper


REQUIRED = ['context', 'device_slot']

BOGUS = [('context', 123, 'unicode string'),
         ('device_slot', '1', 'integer')]


class TestLineResource(s.GetScenarios, s.CreateScenarios, s.EditScenarios, s.DeleteScenarios):

    url = "/lines_sip"
    resource = "Line"
    required = REQUIRED
    bogus_fields = BOGUS

    def create_url(self):
        line = line_helper.add_line(context='default', device_slot=1)
        return "/lines_sip/{}".format(line['id'])
