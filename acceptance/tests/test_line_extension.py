from test_api import helpers as h
from test_api import scenarios as s
from test_api import assertions as a
from test_api import client
from test_api import fixtures
import re


ASSOCIATION_URL = "/lines/{}/extensions"
DISSOCIATION_URL = "/lines/{}/extensions/{}"
EXTENSION_LINE = "/extensions/{}/line"
FAKE_ID = 999999999

not_associated_line_regex = re.compile(r"Extension with id=\d+ does not have a line")
not_associated_user_regex = re.compile(r"line with id \d+ is not associated to a user")
already_associated_msg = "line with id {} already has an extension with a context of type 'internal'"


class TestGetExtensionsFromLine(s.GetScenarios):

    resource = "Line"

    def create_url(self):
        self.line = h.line.generate_line()
        self.extension = h.extension.generate_extension()

        url = ASSOCIATION_URL.format(self.line['id'])
        response = client.post(url, {'extension_id': self.extension['id']})
        response.assert_status(201)

        return url

    def delete_url(self, url):
        client.delete(DISSOCIATION_URL.format(self.line['id'], self.extension['id']))
        h.line.delete_line(self.line['id'])
        h.extension.delete_extension(self.extension['id'])


class TestGetLineFromExtension(TestGetExtensionsFromLine):

    resource = "Extension"

    def create_url(self):
        super(TestGetLineFromExtension, self).create_url()
        return EXTENSION_LINE.format(self.extension['id'])


@fixtures.line()
@fixtures.extension()
def test_get_line_when_not_associated(line, extension):
    response = client.get(EXTENSION_LINE.format(extension['id']))
    a.assert_error(response, not_associated_line_regex)


@fixtures.line()
def test_associate_when_extension_does_not_exist(line):
    url = ASSOCIATION_URL.format(line['id'])
    response = client.post(url, {'extension_id': FAKE_ID})
    a.assert_nonexistent_parameter(response, 'extension_id')


@fixtures.extension()
def test_associate_when_line_does_not_exist(extension):
    url = ASSOCIATION_URL.format(FAKE_ID)
    response = client.post(url, {'extension_id': extension['id']})
    a.assert_nonexistent_parameter(response, 'line_id')


@fixtures.extension('from-extern')
@fixtures.line()
def test_associate_incall_to_line_without_user(incall, line):
    url = ASSOCIATION_URL.format(line['id'])
    response = client.post(url, {'extension_id': incall['id']})
    a.assert_error(response, not_associated_user_regex)


@fixtures.extension()
@fixtures.extension()
@fixtures.line()
def test_associate_two_internal_extensions_to_same_line(first_extension, second_extension, line):
    url = ASSOCIATION_URL.format(line['id'])
    response = client.post(url, {'extension_id': first_extension['id']})
    response.assert_status(201)

    response = client.post(url, {'extension_id': second_extension['id']})
    a.assert_invalid_parameter(response, already_associated_msg.format(line['id']))


@fixtures.line()
def test_dissociate_when_line_does_not_exist(line):
    url = DISSOCIATION_URL.format(line['id'], FAKE_ID)
    response = client.delete(url)
    #we need to standardize status codes on these kinds of errors
    a.assert_error(response, a.nonexistent_regex, 404)
