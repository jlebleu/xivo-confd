from test_api import restapi


def generate_device():
    return add_device()


def add_device(**params):
    response = restapi.devices.post(params)
    return response.item


def delete_device(device_id, check=False):
    response = restapi.devices(device_id).delete()
    if check:
        response.assert_ok()
