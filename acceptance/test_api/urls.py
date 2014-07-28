
URLS = {
    'user.get': '/users/{user_id}',

    'extension_line': '/extensions/{extension_id}/line',

    'line_extension': '/lines/{line_id}/extensions',
    'line_extension.dissociate': '/lines/{line_id}/extensions/{extension_id}',

    'user_line': '/users/{user_id}/lines',
    'user_line.dissociate': '/users/{user_id}/lines/{line_id}',

}


class url_map(object):

    def __init__(self, base):
        self.base = base

    def __call__(self, *args, **kwargs):
        return self.base.format(*args, **kwargs)


def url_for(resource):
    return url_map(URLS[resource])
