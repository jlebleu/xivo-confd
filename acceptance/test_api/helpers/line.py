from test_api import restapi
from test_api import config


def add_line(**params):
    response = restapi.lines_sip.post(params)
    return response.item


def delete_line(line_id, check=False):
    response = restapi.lines_sip(line_id).delete()
    if check:
        response.assert_ok()


def generate_line():
    return add_line(context=config.CONTEXT, device_slot=1)
