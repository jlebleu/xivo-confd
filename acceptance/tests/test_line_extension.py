from test_api.helpers.line import generate_line, delete_line
from test_api.helpers.extension import generate_extension, delete_extension
from test_api.scenarios import GetScenarios, AssociationScenarios
from test_api import assertions as a
from test_api import client, url_for
from test_api import fixtures
import re


associate_url = url_for('line_extension')
dissociate_url = url_for('line_extension.dissociate')
extension_line_url = url_for('extension_line')

FAKE_ID = 999999999

not_associated_line_regex = re.compile(r"Extension with id=\d+ does not have a line")
not_associated_user_regex = re.compile(r"line with id \d+ is not associated to a user")
already_associated_msg = "line with id {} already has an extension with a context of type 'internal'"


class TestGetExtensionsFromLine(GetScenarios):

    resource = "Line"

    def create_url(self):
        self.line = generate_line()
        self.extension = generate_extension()

        url = associate_url(line_id=self.line['id'])
        response = client.post(url, extension_id=self.extension['id'])
        response.assert_status(201)

        return url

    def delete_url(self, url):
        url = dissociate_url(line_id=self.line['id'], extension_id=self.extension['id'])
        client.delete(url)

        delete_line(self.line['id'])
        delete_extension(self.extension['id'])


class TestGetLineFromExtension(TestGetExtensionsFromLine):

    resource = "Extension"

    def create_url(self):
        super(TestGetLineFromExtension, self).create_url()
        return extension_line_url(extension_id=self.extension['id'])


@fixtures.line()
@fixtures.extension()
def test_get_line_when_not_associated(line, extension):
    url = extension_line_url(extension_id=extension['id'])
    response = client.get(url)
    a.assert_error(response, not_associated_line_regex)


@fixtures.line()
def test_associate_when_extension_does_not_exist(line):
    url = associate_url(line_id=line['id'])
    response = client.post(url, extension_id=FAKE_ID)
    a.assert_nonexistent_parameter(response, 'extension_id')


@fixtures.extension()
def test_associate_when_line_does_not_exist(extension):
    url = associate_url(line_id=FAKE_ID)
    response = client.post(url, extension_id=extension['id'])
    a.assert_nonexistent_parameter(response, 'line_id')


@fixtures.extension('from-extern')
@fixtures.line()
def test_associate_incall_to_line_without_user(incall, line):
    url = associate_url(line_id=line['id'])
    response = client.post(url, extension_id=incall['id'])
    a.assert_error(response, not_associated_user_regex)


@fixtures.extension()
@fixtures.extension()
@fixtures.line()
def test_associate_two_internal_extensions_to_same_line(first_extension, second_extension, line):
    url = associate_url(line_id=line['id'])
    response = client.post(url, extension_id=first_extension['id'])
    response.assert_status(201)

    response = client.post(url, extension_id=second_extension['id'])
    #we need to standardize status codes on these kinds of errors
    a.assert_invalid_parameter(response, already_associated_msg.format(line['id']))


@fixtures.line()
def test_dissociate_when_line_does_not_exist(line):
    url = dissociate_url(line_id=line['id'], extension_id=FAKE_ID)
    response = client.delete(url)
    #we need to standardize status codes on these kinds of errors
    a.assert_error(response, a.nonexistent_regex, 404)
