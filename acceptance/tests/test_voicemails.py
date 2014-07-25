from test_api import scenarios as s
from test_api import client


REQUIRED = ['name', 'number', 'context']

BOGUS = [
    ('name', 123, 'unicode string'),
    ('number', 123, 'unicode string'),
    ('context', 123, 'unicode string'),
    ('password', 123, 'unicode string'),
    ('email', 123, 'unicode string'),
    ('language', 123, 'unicode string'),
    ('timezone', 123, 'unicode string'),
    ('max_messages', '3', 'integer'),
    ('attach_audio', 'true', 'boolean'),
    ('delete_messages', 'false', 'boolean'),
    ('ask_password', 'true', 'boolean')
]


def test_errors_on_get():
    scenarios = s.GetErrors("Voicemail",
                            add_voicemail,
                            delete_voicemail)
    scenarios.run()


def test_errors_on_create():
    scenarios = s.CreateErrors("/voicemails",
                               bogus_fields=BOGUS,
                               required=REQUIRED)
    scenarios.run()


def test_errors_on_edit():
    scenarios = s.EditErrors(add_voicemail,
                             delete_voicemail,
                             bogus_fields=BOGUS)
    scenarios.run()


def test_errors_on_delete():
    scenarios = s.DeleteErrors("Voicemail",
                               add_voicemail,
                               delete_voicemail)
    scenarios.run()


def add_voicemail():
    data = {'name': 'myvoicemail',
            'number': '1444',
            'context': 'default'}
    response = client.post("/voicemails", data)
    response.assert_status(201)
    return "/voicemails/{}".format(response.json['id'])


def delete_voicemail(url):
    client.delete(url)
