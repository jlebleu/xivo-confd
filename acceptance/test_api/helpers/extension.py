from test_api import client
from test_api import config


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
