from test_api import client
from test_api.wrappers import IsolatedAction


def add_line(**parameters):
    response = client.post("/lines_sip", parameters)
    response.assert_status(201)
    return response.json


def delete_line(line_id, check=False):
    response = client.delete("/lines_sip/{}".format(line_id))
    if check:
        response.assert_status(204)


class isolated_line(IsolatedAction):

    def __enter__(self):
        self.line = add_line(context='default', device_slot=1)
        return self.line

    def __exit__(self, *args):
        delete_line(self.line['id'], check=False)
