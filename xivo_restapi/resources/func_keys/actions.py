import logging

from flask.helpers import make_response

from xivo_restapi.helpers.formatter import Formatter
from xivo_restapi.resources.func_keys import mapper
from xivo_restapi.helpers import serializer
from xivo_restapi.helpers.common import extract_find_parameters
from xivo_dao.data_handler.func_key.model import FuncKey, FuncKeyOrder
from xivo_dao.data_handler.func_key import services as func_key_services


logger = logging.getLogger(__name__)
formatter = Formatter(mapper, serializer, FuncKey)


def list():
    find_parameters = extract_find_parameters(FuncKeyOrder.mapping())
    search_result = func_key_services.search(**find_parameters)
    result = formatter.list_to_api(search_result.items, search_result.total)
    return make_response(result, 200)


def get(func_key_id):
    func_key = func_key_services.get(func_key_id)
    result = formatter.to_api(func_key)
    return make_response(result, 200)
