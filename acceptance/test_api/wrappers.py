from functools import wraps


class IsolatedAction(object):

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            user = self.__enter__()
            new_args = list(args) + [user]
            result = func(*new_args, **kwargs)
            self.__exit__()
            return result
        return decorated