import requests
import logging
import json
from hamcrest import assert_that, is_in, has_key
from urls import UrlFragment

logger = logging.getLogger(__name__)


class RestApiClient(object):

    @classmethod
    def from_options(cls, host, port, username, password):
        url = "https://{}:{}/1.1".format(host, port)
        return cls(url, username, password)

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False
        self.session.auth = requests.auth.HTTPDigestAuth(username, password)
        self.session.headers = {'Accept': 'application/json',
                                'Content-Type': 'application/json'}

    def request(self, method, url, parameters=None, data=None):
        full_url = self._build_url(url)
        data = self._encode_dict(data)

        logger.info('%s %s params: %s body: %s', method, full_url, parameters, data)
        response = self.session.request(method, full_url, params=parameters, data=data)

        logger.debug('Response - %s %s', response.status_code, response.text)
        return Response(response)

    def get(self, url, **parameters):
        return self.request('GET', url, parameters=parameters)

    def post(self, url, data=None, **kwargs):
        data = data or {}
        data.update(kwargs)
        return self.request('POST', url, data=data)

    def put(self, url, data=None, **kwargs):
        data = data or {}
        data.update(kwargs)
        return self.request('PUT', url, data=data)

    def delete(self, url):
        return self.request('DELETE', url)

    def _encode_dict(self, parameters=None):
        if parameters is not None:
            return json.dumps(parameters)
        return None

    def _build_url(self, url):
        return '/'.join((self.base_url, url.lstrip('/')))

    @property
    def url(self):
        return RestUrlClient(self, [''])


class RestUrlClient(UrlFragment):

    def __init__(self, client, fragments):
        super(RestUrlClient, self).__init__(fragments)
        self.client = client

    def _build(self, fragments):
        return RestUrlClient(self.client, fragments)

    def get(self, **params):
        url = str(self)
        return self.client.get(url, **params)

    def post(self, data=None, **params):
        url = str(self)
        return self.client.post(url, data, **params)

    def put(self, data=None, **params):
        url = str(self)
        return self.client.put(url, data, **params)

    def delete(self):
        url = str(self)
        return self.client.delete(url)


class Response(object):

    STATUS_OK = (200, 201, 204)

    def __init__(self, response):
        self.response = response

    @property
    def raw(self):
        return self.response.text

    @property
    def json(self):
        return self.response.json() if self.response.text else None

    @property
    def item(self):
        self.assert_ok()
        return self.json

    @property
    def items(self):
        self.assert_ok()
        assert_that(self.json, has_key('items'))
        return self.json['items']

    def assert_status(self, *statuses):
        assert_that(self.response.status_code, is_in(statuses), self.response.text)

    def assert_ok(self):
        self.assert_status(*self.STATUS_OK)

    def extract_error(self, regex):
        for msg in self.json:
            if regex.search(msg):
                return msg

        error_msg = "no errors matching '{}'. errors found: {}"
        raise AssertionError(error_msg.format(regex.pattern, self.json))
