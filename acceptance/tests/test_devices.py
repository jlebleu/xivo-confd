from test_api import scenarios as s
from test_api import client


FIELDS = ['ip',
          'mac',
          'sn',
          'vendor',
          'model',
          'version',
          'plugin',
          'description',
          'template_id']

REQUIRED = []

BOGUS = [(f, 123, 'unicode string') for f in FIELDS]


class TestDeviceResource(s.GetScenarios, s.CreateScenarios, s.EditScenarios, s.DeleteScenarios):

    url = "/devices"
    resource = "device"
    required = REQUIRED
    bogus_fields = BOGUS

    def create_url(self):
        response = client.post("/devices", {})
        response.assert_status(201)
        return "/devices/{}".format(response.json['id'])
