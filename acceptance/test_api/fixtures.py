from wrappers import IsolatedAction

from helpers.user import generate_user, delete_user
from helpers.line import generate_line, delete_line
from helpers.extension import generate_extension, delete_extension
from helpers.device import generate_device, delete_device
from helpers.voicemail import generate_voicemail, delete_voicemail


class user(IsolatedAction):

    actions = {'generate': generate_user,
               'delete': delete_user}


class line(IsolatedAction):

    actions = {'generate': generate_line,
               'delete': delete_line}


class extension(IsolatedAction):

    actions = {'generate': generate_extension,
               'delete': delete_extension}


class device(IsolatedAction):

    actions = {'generate': generate_device,
               'delete': delete_device}


class voicemail(IsolatedAction):

    actions = {'generate': generate_voicemail,
               'delete': delete_voicemail}
