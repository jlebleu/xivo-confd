from test_api import client
from test_api import config


def add_line(**parameters):
    response = client.post("/lines_sip", parameters)
    return response.item


def delete_line(line_id, check=False):
    response = client.delete("/lines_sip/{}".format(line_id))
    if check:
        response.assert_ok()


def generate_line():
    return add_line(context=config.CONTEXT, device_slot=1)
