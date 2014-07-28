from test_api import client, url_for
from test_api import helpers as h
from test_api import assertions as a
from test_api import scenarios as s
from test_api import fixtures

from contextlib import contextmanager


FAKE_ID = 999999999

associate_url = url_for('user_line')
dissociate_url = url_for('user_line.dissociate')
user_url = url_for('user.get')

class TestUserLineResource(s.CreateScenarios):

    resource = "UserLine"
    url = associate_url(user_id=FAKE_ID)
    required = ['line_id']
    bogus_fields = [('line_id', '123', 'integer')]


@contextmanager
def user_and_line_associated(user, line):
    url = associate_url(user_id=user['id'])
    response = client.post(url, line_id=line['id'])
    response.assert_status(201)

    yield

    url = dissociate_url(user_id=user['id'], line_id=line['id'])
    client.delete(url)


@fixtures.line()
def test_get_when_user_does_not_exist(line):
    url = associate_url(user_id=FAKE_ID)
    response = client.get(url)
    a.assert_not_exists(response, 'User')


@fixtures.line()
def test_associate_when_user_does_not_exist(line):
    url = associate_url(user_id=FAKE_ID)
    response = client.post(url, line_id=line['id'])
    a.assert_nonexistent_parameter(response, 'user_id')


@fixtures.user()
def test_associate_when_line_does_not_exist(user):
    url = associate_url(user_id=user['id'])
    response = client.post(url, line_id=FAKE_ID)
    a.assert_nonexistent_parameter(response, 'line_id')


@fixtures.user()
@fixtures.line()
def test_associate_when_user_already_associated_to_same_line(user, line):
    with user_and_line_associated(user, line):
        url = associate_url(user_id=user['id'])
        response = client.post(url, line_id=line['id'])
        a.assert_invalid_parameter(response, 'user is already associated to this line')


@fixtures.user()
@fixtures.line()
@fixtures.line()
def test_associate_when_user_already_associated_to_another_line(user, first_line, second_line):
    with user_and_line_associated(user, first_line):
        url = associate_url(user_id=user['id'])
        response = client.post(url, {'line_id': second_line['id']})
        a.assert_invalid_parameter(response, 'user is already associated to this line')


@fixtures.user()
@fixtures.line()
def test_dissociate_when_not_associated(user, line):
    url = dissociate_url(user_id=user['id'], line_id=line['id'])
    response = client.delete(url)
    a.assert_not_associated(response, 'User', 'line')


@fixtures.line()
def test_dissociate_when_user_does_not_exist(line):
    url = dissociate_url(user_id=FAKE_ID, line_id=line['id'])
    response = client.delete(url)
    a.assert_not_associated(response, 'User', 'line')


@fixtures.user()
@fixtures.user()
@fixtures.line()
def test_dissociate_second_user_before_first(first_user, second_user, line):
    with user_and_line_associated(first_user, line), user_and_line_associated(second_user, line):
        url = dissociate_url(user_id=first_user['id'], line_id=line['id'])
        response = client.delete(url)
        a.assert_invalid_parameter(response, 'There are secondary users associated to this line')


@fixtures.user()
@fixtures.line()
def test_delete_user_when_user_and_line_associated(user, line):
    with user_and_line_associated(user, line):
        url = user_url(user_id=user['id'])
        response = client.delete(url)
        a.assert_delete_error(response, 'User', 'user still associated to a line')
