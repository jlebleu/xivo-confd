from test_api import restapi
from test_api import config


def generate_extension(context=config.CONTEXT):
    exten = find_available_exten(context)
    return add_extension(exten=exten, context=context)


def find_available_exten(context):
    response = restapi.extensions.get()
    numbers = [int(e['exten'])
               for e in response.items
               if e['context'] == context and e['exten'].isdigit()]

    available = set(config.EXTENSION_RANGE) - set(numbers)
    return str(available.pop())


def add_extension(**params):
    response = restapi.extensions.post(params)
    return response.item


def delete_extension(extension_id, check=False):
    response = restapi.extensions(extension_id).delete()
    if check:
        response.assert_ok()
