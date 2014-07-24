from test_api import client


def add_user(**parameters):
    response = client.post("/users", parameters)
    response.assert_status(201)
    return response.json


def delete_user(user_id):
    response = client.delete("/users/{}".format(user_id))
    response.assert_status(204)
