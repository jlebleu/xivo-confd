from test_api import restapi


def add_user(**params):
    response = restapi.users.post(params)
    return response.item


def delete_user(user_id, check=False):
    response = restapi.users(user_id).delete()
    if check:
        response.assert_ok()


def generate_user():
    return add_user(firstname='John', lastname='Doe')
