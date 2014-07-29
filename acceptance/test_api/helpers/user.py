from test_api import client


def add_user(**parameters):
    response = client.post("/users", parameters)
    return response.item


def delete_user(user_id, check=False):
    response = client.delete("/users/{}".format(user_id))
    if check:
        response.assert_ok()


def generate_user():
    return add_user(firstname='John', lastname='Doe')
