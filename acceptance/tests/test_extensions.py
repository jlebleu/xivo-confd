from test_api import scenarios as s
from test_api import client


REQUIRED = ['exten', 'context']

BOGUS = [('exten', 123, 'unicode string'),
         ('context', 123, 'unicode string'),
         ('commented', 'true', 'boolean')]


def test_errors_on_get():
    scenarios = s.GetErrors("Extension",
                            add_extension,
                            delete_extension)
    scenarios.run()


def test_errors_on_create():
    scenarios = s.CreateErrors("/extensions",
                               bogus_fields=BOGUS,
                               required=REQUIRED)
    scenarios.run()


def test_errors_on_edit():
    scenarios = s.EditErrors(add_extension,
                             delete_extension,
                             bogus_fields=BOGUS)
    scenarios.run()


def test_errors_on_delete():
    scenarios = s.DeleteErrors("Extension",
                               add_extension,
                               delete_extension)
    scenarios.run()


def add_extension():
    response = client.post("/extensions", {'context': 'default', 'exten': '1444'})
    response.assert_status(201)
    return "/extensions/{}".format(response.json['id'])


def delete_extension(url):
    client.delete(url)
