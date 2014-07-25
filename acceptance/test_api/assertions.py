from hamcrest import assert_that, contains_string, equal_to
import re


missing_regex = re.compile(r"Missing parameters: (([\w_-]+)(,([\w_-]+))*)")
invalid_regex = re.compile(r"Invalid parameters: (.+)")
validation_regex = re.compile(r"Error while validating field '([\w_-]+)': '(.*?)' is not an? (.+)")
not_exists_regex = re.compile(r"([\w_-]+) with [\w_]*id=(\w+) does not exist")
nonexistent_regex = re.compile(r"Nonexistent parameters: ([\w_-]+) \w+ does not exist")
not_associated_regex = re.compile(r"([\w_-]+) with id=\w+ is not associated with ([\w_-]+) id=\w+")
delete_regex = re.compile(r"Error while deleting ([\w_-]+): (.+)")


def assert_missing_parameter(response, name):
    response.assert_status(400)
    error = response.extract_error(missing_regex)
    assert_that(error, contains_string(name))


def assert_invalid_parameter(response, name):
    response.assert_status(400)
    error = response.extract_error(invalid_regex)
    assert_that(error, contains_string(name))


def assert_field_validation(response, expected_name, expected_type):
    response.assert_status(400)
    error = response.extract_error(validation_regex)
    match = validation_regex.match(error)

    name = match.group(1)
    field_type = match.group(3)

    assert_that(name, equal_to(expected_name))
    assert_that(field_type, equal_to(expected_type))


def assert_not_exists(response, expected_resource):
    response.assert_status(404)
    error = response.extract_error(not_exists_regex)

    resource = not_exists_regex.match(error).group(1)
    assert_that(resource, equal_to(expected_resource))


def assert_nonexistent_parameter(response, expected_field):
    response.assert_status(400)
    error = response.extract_error(nonexistent_regex)
    match = nonexistent_regex.match(error)

    field_name = match.group(1)
    assert_that(field_name, equal_to(expected_field))


def assert_not_associated(response, expected_left, expected_right):
    response.assert_status(404)
    error = response.extract_error(not_associated_regex)
    match = not_associated_regex.match(error)

    left, right = match.groups([1, 2])
    assert_that(left, equal_to(expected_left))
    assert_that(right, equal_to(expected_right))


def assert_delete_error(response, expected_resource, expected_message):
    response.assert_status(400)
    error = response.extract_error(delete_regex)
    match = delete_regex.match(error)

    resource, message = match.groups([1, 2])
    assert_that(resource, equal_to(expected_resource))
    assert_that(message, equal_to(expected_message))
