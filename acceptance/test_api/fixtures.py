import config
from wrappers import IsolatedAction

from helpers.user import generate_user, delete_user
from helpers.line import generate_line, delete_line
from helpers.extension import generate_extension, delete_extension


class user(IsolatedAction):

    def __enter__(self):
        self.user = generate_user()
        return self.user

    def __exit__(self, *args):
        delete_user(self.user['id'], check=False)


class line(IsolatedAction):

    def __enter__(self):
        self.line = generate_line()
        return self.line

    def __exit__(self, *args):
        delete_line(self.line['id'], check=False)


class extension(IsolatedAction):

    def __init__(self, context=config.CONTEXT):
        super(extension, self).__init__()
        self.context = context

    def __enter__(self):
        self.extension = generate_extension(self.context)
        return self.extension

    def __exit__(self, *args):
        delete_extension(self.extension['id'])
