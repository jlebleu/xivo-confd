class UrlFragment(object):

    @classmethod
    def new(cls, base=''):
        return cls([base])

    def __init__(self, fragments):
        self.fragments = fragments

    def __call__(self, value=None, param=None):
        return self._build(self._add(value, param))

    def __getattr__(self, name):
        return self._build(self._add(name))

    def __str__(self):
        full_url = '/'.join(self.fragments)
        return full_url

    def __repr__(self):
        return '<UrlFragment {} {}>'.format(str(self), self.fragments)

    def apply(self, **kwargs):
        fragments = [f.format(**kwargs) for f in self.fragments]
        return self._build(fragments)

    def _build(self, fragments):
        return self.__class__(fragments)

    def _add(self, value=None, param=None):
        if value and param:
            raise ValueError("value and param are mutually exclusive")
        if value:
            return self.fragments + [str(value)]
        if param:
            return self.fragments + ['{{{}}}'.format(param)]
        return self.fragments
