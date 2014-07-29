from test_api import restapi
from test_api import config


def generate_voicemail(context=config.CONTEXT):
    number = find_available_number(context)
    return add_voicemail(name='myvoicemail',
                         number=number,
                         context=context)


def find_available_number(context):
    response = restapi.voicemails.get()
    numbers = [int(v['number'])
               for v in response.items
               if v['context'] == context and v['number'].isdigit()]

    available_numbers = set(config.EXTENSION_RANGE) - set(numbers)
    return str(available_numbers.pop())


def add_voicemail(**params):
    response = restapi.voicemails.post(params)
    return response.item


def delete_voicemail(voicemail_id, check=False):
    response = restapi.voicemails(voicemail_id).delete()
    if check:
        response.assert_ok()
