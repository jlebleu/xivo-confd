import requests
import logging
import json
from hamcrest import assert_that, is_in, has_key

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

        logger.debug('Request - %s %s params: %s body: %s', method, full_url, parameters, data)
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


class Response(object):

    def __init__(self, response):
        self.response = response

    @property
    def json(self):
        return self.response.json() if self.response.text else None

    @property
    def raw(self):
        return self.response.text

    def assert_status(self, *statuses):
        assert_that(self.response.status_code, is_in(statuses), self.response.text)

    def assert_regex(self, regex):
        msg = "'%s' does not match on '%s'" % (regex.pattern, self.response.text)
        assert_that(regex.search(self.response.text), msg)

    def extract_error(self, regex):
        for msg in self.json:
            if regex.search(msg):
                return msg
        raise AssertionError("did not find any error message matching '%s'" % regex.pattern)

    @property
    def content(self):
        self.assert_status(200, 201, 204)
        return self.json

    @property
    def item(self):
        return self.content

    @property
    def items(self):
        assert_that(self.content, has_key('items'))
        return self.content['items']
