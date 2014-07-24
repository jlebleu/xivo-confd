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


def test_errors_on_get():
    scenarios = s.GetErrors("device",
                            add_device,
                            delete_device)
    scenarios.run()


def test_errors_on_create():
    scenarios = s.CreateErrors("/devices",
                               bogus_fields=BOGUS,
                               required=REQUIRED)
    scenarios.run()


def test_errors_on_edit():
    scenarios = s.EditErrors(add_device,
                             delete_device,
                             bogus_fields=BOGUS)
    scenarios.run()


def test_errors_on_delete():
    scenarios = s.DeleteErrors("device",
                               add_device,
                               delete_device)
    scenarios.run()


def add_device():
    response = client.post("/devices", {})
    response.assert_status(201)
    return "/devices/{}".format(response.json['id'])


def delete_device(url):
    client.delete(url)
