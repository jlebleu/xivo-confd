
URLS = {
    'user.get': '/users/{user_id}',

    'extension_line.get': '/extensions/{extension_id}/line',

    'line_extension.list': '/lines/{line_id}/extensions',
    'line_extension.associate': '/lines/{line_id}/extensions',
    'line_extension.dissociate': '/lines/{line_id}/extensions/{extension_id}',

    'user_line.list': '/users/{user_id}/lines',
    'user_line.associate': '/users/{user_id}/lines',
    'user_line.dissociate': '/users/{user_id}/lines/{line_id}',

}


class url_map(object):

    def __init__(self, base):
        self.base = base

    def __call__(self, *args, **kwargs):
        return self.base.format(*args, **kwargs)

    def __str__(self):
        return self.base


def url_for(resource):
    return url_map(URLS[resource])
