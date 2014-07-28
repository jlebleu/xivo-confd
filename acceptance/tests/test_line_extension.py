from test_api.helpers.line import generate_line, delete_line
from test_api.helpers.extension import generate_extension, delete_extension
from test_api.scenarios import AssociationScenarios, DissociationScenarios, AssociationGetScenarios
from test_api import assertions as a
from test_api import client, url_for
from test_api import fixtures
import re
import unittest


list_url = url_for('line_extension.list')
associate_url = url_for('line_extension.associate')
dissociate_url = url_for('line_extension.dissociate')
extension_line_url = url_for('extension_line.get')

FAKE_ID = 999999999

no_line_associated_regex = re.compile(r"Extension with id=\d+ does not have a line")
no_user_associated_regex = re.compile(r"line with id \d+ is not associated to a user")
already_associated_regex = re.compile(r"line with id \d+ already has an extension with a context of type 'internal'")
not_associated_regex = re.compile(r"Line \(id=\d+\) is not associated with Extension \(id=\d+\)")


class LineExtensionAssociation(object):

    left_resource = "Line"
    right_resource = "Extension"
    left_field = 'line_id'
    right_field = 'extension_id'
    associated_error = already_associated_regex
    not_associated_error = not_associated_regex

    def create_resources(self):
        line = generate_line()
        extension = generate_extension()
        return line['id'], extension['id']

    def delete_resources(self, line_id, extension_id):
        delete_line(line_id)
        delete_extension(extension_id)

    def associate_resources(self, line_id, extension_id):
        url = associate_url(line_id=line_id)
        return client.post(url, extension_id=extension_id)

    def dissociate_resources(self, line_id, extension_id):
        url = dissociate_url(line_id=line_id, extension_id=extension_id)
        return client.delete(url)

    def get_association(self, line_id, extension_id):
        url = list_url(line_id=line_id, extension_id=extension_id)
        return client.get(url)


class TestLineExtensionAssociation(LineExtensionAssociation, AssociationScenarios, DissociationScenarios, AssociationGetScenarios):

    association_error_regex = already_associated_regex
    not_associated_error_regex = not_associated_regex

    @unittest.skip("will be fixed after refactoring DAO exceptions")
    def test_dissociation_when_right_does_not_exist(self):
        pass


@fixtures.line()
@fixtures.extension()
def test_get_line_from_extension_when_not_associated(line, extension):
    url = extension_line_url(extension_id=extension['id'])
    response = client.get(url)
    a.assert_error(response, no_line_associated_regex)


@fixtures.extension('from-extern')
@fixtures.line()
def test_associate_incall_to_line_without_user(incall, line):
    url = associate_url(line_id=line['id'])
    response = client.post(url, extension_id=incall['id'])
    a.assert_error(response, no_user_associated_regex)


@fixtures.extension()
@fixtures.extension()
@fixtures.line()
def test_associate_two_internal_extensions_to_same_line(first_extension, second_extension, line):
    url = associate_url(line_id=line['id'])
    response = client.post(url, extension_id=first_extension['id'])
    response.assert_status(201)

    response = client.post(url, extension_id=second_extension['id'])
    #we need to standardize status codes on these kinds of errors
    a.assert_error(response, already_associated_regex, 400)
