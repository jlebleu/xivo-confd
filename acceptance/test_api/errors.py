import re

from collections import namedtuple

ExpectedStatus = namedtuple('ExpectedStatus', ['status', 'regex'])


def missing_parameters(param_name):
    return ExpectedStatus(400, re.compile(r"Missing Parameters: "))
