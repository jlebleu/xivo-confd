import config
from wrappers import IsolatedAction

from helpers.user import generate_user, delete_user
from helpers.line import generate_line, delete_line
from helpers.extension import generate_extension, delete_extension


class user(IsolatedAction):

    actions = {'generate': generate_user,
               'delete': delete_user}


class line(IsolatedAction):

    actions = {'generate': generate_line,
               'delete': delete_line}


class extension(IsolatedAction):

    actions = {'generate': generate_extension,
               'delete': delete_extension}


