from test_api import client
import assertions as a


class TestContext(object):

    def __init__(self, setup, teardown=None):
        self.setup = setup
        self.teardown = teardown

    def __enter__(self):
        self.url = self.setup()
        return self.url

    def __exit__(self, *args):
        if self.teardown:
            self.teardown(self.url)


class GetErrors(object):

    def __init__(self, resource, setup, teardown):
        self.resource = resource
        self.setup = setup
        self.teardown = teardown

    def run(self):
        url = self.setup()
        self.teardown(url)

        response = client.get(url)
        a.assert_not_exists(response, self.resource)


class CreateErrors(object):

    def __init__(self, url, required=None, bogus_fields=None):
        self.url = url
        self.required = required or []
        self.bogus_fields = bogus_fields or []

    def run(self):
        self.check_missing()
        self.check_invalid()
        self.check_wrong_type()

    def check_missing(self):
        for field in self.required:
            response = client.post(self.url, {})
            a.assert_missing_parameter(response, field)

    def check_invalid(self):
        response = client.post(self.url, {'invalid': 'invalid'})
        a.assert_invalid_parameter(response, 'invalid')

    def check_wrong_type(self):
        for field, value, message in self.bogus_fields:
            response = client.post(self.url, {field: value})
            a.assert_field_validation(response, field, message)


class EditErrors(object):

    def __init__(self, setup, teardown, bogus_fields=None):
        self.setup = setup
        self.test_context = TestContext(setup, teardown)
        self.bogus_fields = bogus_fields or []

    def run(self):
        self.check_invalid()
        self.check_wrong_type()

    def check_invalid(self):
        with self.test_context as url:
            response = client.put(url, {'invalid': 'invalid'})
            a.assert_invalid_parameter(response, 'invalid')

    def check_wrong_type(self):
        with self.test_context as url:
            for field, value, message in self.bogus_fields:
                response = client.put(url, {field: value})
                a.assert_field_validation(response, field, message)


class DeleteErrors(object):

    def __init__(self, resource, setup, teardown):
        self.resource = resource
        self.setup = setup
        self.teardown = teardown

    def run(self):
        url = self.setup()
        self.teardown(url)

        response = client.delete(url)
        a.assert_not_exists(response, self.resource)
