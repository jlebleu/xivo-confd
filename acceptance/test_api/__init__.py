from xivo_lettuce.config import read_config
from restapi_client import RestApiClient

from urls import url_for, url_map

client = None


def setup():
    global client

    config = read_config()
    client = RestApiClient.from_options(
        config.get('xivo', 'hostname'),
        config.get('restapi', 'port'),
        config.get('webservices_infos', 'login'),
        config.get('webservices_infos', 'password'))
