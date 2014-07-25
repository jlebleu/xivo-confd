from test_api import client
from test_api.wrappers import IsolatedAction


def add_user(**parameters):
    response = client.post("/users", parameters)
    return response.item


def delete_user(user_id, check=False):
    response = client.delete("/users/{}".format(user_id))
    if check:
        response.assert_status(204)


def generate_user():
    return add_user(firstname='John', lastname='Doe')


class isolated_user(IsolatedAction):

    def __enter__(self):
        self.user = generate_user()
        return self.user

    def __exit__(self, *args):
        delete_user(self.user['id'], check=False)
