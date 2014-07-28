from contextlib import contextmanager

from test_api import client
import assertions as a


class Scenarios(object):

    resource = None
    required = []
    bogus_fields = []

    @contextmanager
    def generated_url(self):
        url = self.create_url()
        yield url
        self.delete_url(url)

    def delete_url(self, url):
        client.delete(url)


class GetScenarios(Scenarios):

    def test_resource_does_not_exist_on_get(self):
        url = self.create_url()
        self.delete_url(url)

        response = client.get(url)
        a.assert_not_exists(response, self.resource)


class CreateScenarios(Scenarios):

    def test_missing_parameter(self):
        for field in self.required:
            response = client.post(self.url, {})
            yield a.assert_missing_parameter, response, field

    def test_invalid_parameter_on_post(self):
        response = client.post(self.url, {'invalid': 'invalid'})
        a.assert_invalid_parameter(response, 'invalid')

    def test_wrong_parameter_type_on_post(self):
        for bogus_field in self.bogus_fields:
            yield self.check_bogus_field_on_post, bogus_field

    def check_bogus_field_on_post(self, bogus_field):
        field, value, message = bogus_field
        response = client.post(self.url, {field: value})
        a.assert_field_validation(response, field, message)


class EditScenarios(Scenarios):

    def test_invalid_parameter_on_put(self):
        with self.generated_url() as url:
            response = client.put(url, {'invalid': 'invalid'})
            a.assert_invalid_parameter(response, 'invalid')

    def test_wrong_parameter_type_on_put(self):
        with self.generated_url() as url:
            for bogus_field in self.bogus_fields:
                yield self.check_bogus_field_on_put, url, bogus_field

    def check_bogus_field_on_put(self, url, bogus_field):
        field, value, message = bogus_field
        response = client.put(url, {field: value})
        a.assert_field_validation(response, field, message)


class DeleteScenarios(Scenarios):

    def test_resource_does_not_exist_on_delete(self):
        url = self.create_url()
        self.delete_url(url)

        response = client.delete(url)
        a.assert_not_exists(response, self.resource)


class RelationScenario(object):

    FAKE_ID = 999999999

    left_resource = None
    left_field = None
    right_resource = None
    right_field = None
    associated_error = None
    not_associated_erorr = None

    @contextmanager
    def generated_resources(self):
        left_id, right_id = self.create_resources()
        yield left_id, right_id
        self.delete_resources(left_id, right_id)


class AssociationScenarios(RelationScenario):

    def test_association_when_left_does_not_exist(self):
        with self.generated_resources() as (left_id, right_id):
            response = self.associate_resources(self.FAKE_ID, right_id)
            a.assert_nonexistent_parameter(response, self.left_field)

    def test_association_when_right_does_not_exist(self):
        with self.generated_resources() as (left_id, right_id):
            response = self.associate_resources(left_id, self.FAKE_ID)
            a.assert_nonexistent_parameter(response, self.right_field)

    def test_association_when_resources_already_associated(self):
        with self.generated_resources() as (left_id, right_id):
            response = self.associate_resources(left_id, right_id)
            response.assert_status(201)

            response = self.associate_resources(left_id, right_id)
            a.assert_error(response, self.associated_error, 400)


class AssociationGetScenarios(RelationScenario):

    def test_get_association_when_left_does_not_exist(self):
        with self.generated_resources() as (left_id, right_id):
            response = self.get_association(self.FAKE_ID, right_id)
            a.assert_not_exists(response, self.left_resource)


class DissociationScenarios(RelationScenario):

    def test_dissociation_when_left_does_not_exist(self):
        with self.generated_resources() as (left_id, right_id):
            response = self.dissociate_resources(self.FAKE_ID, right_id)
            a.assert_nonexistent_parameter(response, self.left_field, 404)

    def test_dissociation_when_right_does_not_exist(self):
        with self.generated_resources() as (left_id, right_id):
            response = self.dissociate_resources(left_id, self.FAKE_ID)
            a.assert_nonexistent_parameter(response, self.right_field, 400)

    def test_dissociation_when_not_associated(self):
        with self.generated_resources() as (left_id, right_id):
            response = self.dissociate_resources(left_id, right_id)
            a.assert_error(response, self.not_associated_error, 400)
