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
