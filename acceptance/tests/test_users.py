from test_api import scenarios as s
from test_api.helpers import user as user_helper
from test_api import client

FIELDS = ['firstname',
          'lastname',
          'timezone',
          'language',
          'description',
          'caller_id',
          'outgoing_caller_id',
          'mobile_phone_number',
          'username',
          'password',
          'music_on_hold',
          'preprocess_subroutine',
          'userfield']

REQUIRED = ['firstname']

BOGUS = [(f, 123, 'unicode string') for f in FIELDS]


def test_errors_on_get():
    scenarios = s.GetErrors("User",
                            add_user,
                            delete_user)
    scenarios.run()


def test_errors_on_create():
    scenarios = s.CreateErrors("/users",
                               bogus_fields=BOGUS,
                               required=REQUIRED)
    scenarios.run()


def test_errors_on_edit():
    scenarios = s.EditErrors(add_user,
                             delete_user,
                             bogus_fields=BOGUS)
    scenarios.run()


def test_errors_on_delete():
    scenarios = s.DeleteErrors("User",
                               add_user,
                               delete_user)
    scenarios.run()


def add_user():
    user = user_helper.add_user(firstname='firstname')
    return "/users/{}".format(user['id'])


def delete_user(url):
    client.delete(url)
