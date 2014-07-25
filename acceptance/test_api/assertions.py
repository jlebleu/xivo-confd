from hamcrest import assert_that, contains_string, equal_to
import re


missing_regex = re.compile(r"Missing parameters: (([\w_-]+)(,([\w_-]+))*)")
invalid_regex = re.compile(r"Invalid parameters: (.+)")
validation_regex = re.compile(r"Error while validating field '([\w_-]+)': '(.*?)' is not an? (.+)")
not_exists_regex = re.compile(r"([\w_-]+) with [\w_]*id=(\w+) does not exist")
nonexistent_regex = re.compile(r"Nonexistent parameters: ([\w_-]+) \w+ does not exist")
not_associated_regex = re.compile(r"([\w_-]+) with id=\w+ is not associated with ([\w_-]+) id=\w+")
delete_regex = re.compile(r"Error while deleting ([\w_-]+): (.+)")


def assert_error(response, regex, *statuses):
    statuses = statuses or (400, 404)
    response.assert_status(*statuses)
    error = response.extract_error(regex)
    return regex.match(error)


def assert_missing_parameter(response, name):
    match = assert_error(response, missing_regex, 400)
    assert_that(match.group(1), contains_string(name))


def assert_invalid_parameter(response, name):
    match = assert_error(response, invalid_regex, 400)
    assert_that(match.group(1), contains_string(name))


def assert_field_validation(response, expected_name, expected_type):
    match = assert_error(response, validation_regex, 400)
    name = match.group(1)
    field_type = match.group(3)
    assert_that(name, equal_to(expected_name))
    assert_that(field_type, equal_to(expected_type))


def assert_not_exists(response, expected_resource):
    match = assert_error(response, not_exists_regex, 404)
    assert_that(match.group(1), equal_to(expected_resource))


def assert_nonexistent_parameter(response, expected_field):
    match = assert_error(response, nonexistent_regex, 400)
    assert_that(match.group(1), equal_to(expected_field))


def assert_not_associated(response, expected_left, expected_right):
    match = assert_error(response, not_associated_regex, 404)
    left, right = match.groups([1, 2])
    assert_that(left, equal_to(expected_left))
    assert_that(right, equal_to(expected_right))


def assert_delete_error(response, expected_resource, expected_message):
    match = assert_error(response, delete_regex, 400)
    resource, message = match.groups([1, 2])
    assert_that(resource, equal_to(expected_resource))
    assert_that(message, equal_to(expected_message))
