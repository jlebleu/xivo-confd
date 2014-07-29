from test_api import scenarios as s
from test_api import restapi
from test_api.helpers.device import generate_device


FIELDS = ['ip',
          'mac',
          'sn',
          'vendor',
          'model',
          'version',
          'plugin',
          'description',
          'template_id']


BOGUS = [(f, 123, 'unicode string') for f in FIELDS]


class TestDeviceResource(s.GetScenarios, s.CreateScenarios, s.EditScenarios, s.DeleteScenarios):

    url = "/devices"
    resource = "device"
    required = []
    bogus_fields = BOGUS

    def create_url(self):
        device = generate_device()
        url = restapi.devices(device['id'])
        return str(url)
