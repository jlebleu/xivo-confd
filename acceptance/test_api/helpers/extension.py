from test_api import client
from test_api import config
from test_api.wrappers import IsolatedAction


def generate_extension(context=config.CONTEXT):
    exten = find_available_exten(context, config.EXTENSION_RANGE)
    return add_extension(exten=exten, context=context)


def find_available_exten(context, number_range):
    response = client.get("/extensions")
    numbers = [int(e['exten'])
               for e in response.items
               if e['context'] == context and e['exten'].isdigit()]

    return str((set(number_range) - set(numbers)).pop())


def add_extension(**params):
    response = client.post("/extensions", params)
    return response.item


def delete_extension(extension_id, check=False):
    response = client.delete("/extensions/{}".format(extension_id))
    if check:
        response.assert_status(204)


class isolated_extension(IsolatedAction):

    def __init__(self, context=config.CONTEXT):
        super(isolated_extension, self).__init__()
        self.context = context

    def __enter__(self):
        self.extension = generate_extension(self.context)
        return self.extension

    def __exit__(self, *args):
        delete_extension(self.extension['id'])
