from test_api import scenarios as s
from test_api import client


REQUIRED = ['context', 'device_slot']

BOGUS = [('context', 123, 'unicode string'),
         ('device_slot', '1', 'integer')]


def test_errors_on_get():
    scenarios = s.GetErrors("Line",
                            add_line,
                            delete_line)
    scenarios.run()


def test_errors_on_create():
    scenarios = s.CreateErrors("/lines_sip",
                               bogus_fields=BOGUS,
                               required=REQUIRED)
    scenarios.run()


def test_errors_on_edit():
    scenarios = s.EditErrors(add_line,
                             delete_line,
                             bogus_fields=BOGUS)
    scenarios.run()


def test_errors_on_delete():
    scenarios = s.DeleteErrors("Line",
                               add_line,
                               delete_line)
    scenarios.run()


def add_line():
    response = client.post("/lines_sip", {'context': 'default', 'device_slot': 1})
    response.assert_status(201)
    return "/lines_sip/{}".format(response.json['id'])


def delete_line(url):
    client.delete(url)
