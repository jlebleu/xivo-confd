Feature: REST API Extensions

    Scenario: Extension list with one extension
        Given I have the following extensions:
            | exten | context |
            | 1523  | default |
        When I access the list of extensions
        Then I get a list containing the following extensions:
            | exten | context |
            | 1523  | default |

    Scenario: Extension list with two extensions
        Given I have the following extensions:
            | exten | context |
            | 1983  | default |
            | 1947  | default |
        When I access the list of extensions
        Then I get a list containing the following extensions:
            | exten | context |
            | 1983  | default |
            | 1947  | default |

    Scenario: Get an extension that does not exist
        When I access a fake extension id
        Then I get a response with status "404"

    Scenario: Get an extension
        Given I have the following extensions:
            | exten | context |
            | 1599  | default |
        When I access the extension with exten "1599@default"
        Then I get a response with status "200"
        Then I have an extension with the following parameters:
            | exten | context |
            | 1599  | default |
        Then I get a response with an id
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an empty extension
        When I create an empty extension
        Then I get a response with status "400"
        Then I get an error message "Missing parameters: exten,context"

    Scenario: Creating an extension with an empty number
        When I create an extension with the following parameters:
            | exten | context |
            |       | default |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: Exten required"

    Scenario: Creating an extension with an empty context
        When I create an extension with the following parameters:
            | exten | context |
            | 1000  |         |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: Context required"

    Scenario: Creating an extension with only the number
        When I create an extension with the following parameters:
            | exten |
            | 1000  |
        Then I get a response with status "400"
        Then I get an error message "Missing parameters: context"

    Scenario: Creating an extension with only the context
        When I create an extension with the following parameters:
            | context |
            | default |
        Then I get a response with status "400"
        Then I get an error message "Missing parameters: exten"

    Scenario: Creating an extension with invalid parameters
        When I create an extension with the following parameters:
            | toto |
            | tata |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: toto"

    Scenario: Creating a commented extension
        Given I have no extension with exten "1883@default"
        When I create an extension with the following parameters:
            | exten | context | commented |
            | 1883  | default | true      |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension that isn't commented
        Given I have no extension with exten "1294@default"
        When I create an extension with the following parameters:
            | exten | context | commented |
            | 1294  | default | false     |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in user range
        Given I have no extension with exten "1000@default"
        When I create an extension with the following parameters:
            | exten | context |
            | 1000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in group range
        Given I have no extension with exten "2000@default"
        When I create an extension with the following parameters:
            | exten | context |
            | 2000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in queue range
        Given I have no extension with exten "3000@default"
        When I create an extension with the following parameters:
            | exten | context |
            | 3000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in conference room range
        Given I have no extension with exten "4000@default"
        When I create an extension with the following parameters:
            | exten | context |
            | 4000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in incall range
        Given I have no extension with exten "3954@from-extern"
        When I create an extension with the following parameters:
            | exten | context     |
            |  3954 | from-extern |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an alphanumeric extension
        When I create an extension with the following parameters:
            | exten  | context |
            | ABC123 | default |
        Then I get a response with status "400"
        Then i get an error message "Invalid parameters: Alphanumeric extensions are not supported"

    Scenario: Creating twice the same extension
        Given I have no extension with exten "1454@default"
        When I create an extension with the following parameters:
            | exten | context |
            | 1454  | default |
        Then I get a response with status "201"
        When I create an extension with the following parameters:
            | exten | context |
            | 1454  | default |
        Then I get a response with status "400"
        Then I get an error message "Extension 1454@default already exists"

    Scenario: Creating two extensions in different contexts
        Given I have no extension with exten "1119@default"
        Given I have no extension with exten "1119@from-extern"
        When I create an extension with the following parameters:
            | exten | context |
            | 1119  | default |
        Then I get a response with status "201"
        When I create an extension with the following parameters:
            | exten | context     |
            | 1119  | from-extern |
        Then I get a response with status "201"

    Scenario: Creating an extension with a context that doesn't exist
        When I create an extension with the following parameters:
            | exten | context             |
            | 1000  | mysuperdupercontext |
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: context mysuperdupercontext does not exist"

    Scenario: Creating an extension outside of context range
        When I create an extension with the following parameters:
            | exten | context |
            | 99999 | default |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: exten 99999 not inside range of context default"

    Scenario: Editing an extension that doesn't exist
        When I update a fake extension
        Then I get a response with status "404"

    Scenario: Editing an extension with parameters that don't exist
        Given I have the following extensions:
          | exten | context |
          | 1358  | default |
        When I update the extension with exten "1358@default" using the following parameters:
          | unexisting_field |
          | unexisting value |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: unexisting_field"

    Scenario: Editing the exten of a extension
        Given I have no extension with exten "1145@default"
        Given I have the following extensions:
          | exten | context |
          | 1045  | default |
        When I update the extension with exten "1045@default" using the following parameters:
          | exten |
          | 1145  |
        Then I get a response with status "204"
        When I access the extension with exten "1145@default"
        Then I have an extension with the following parameters:
          | exten | context |
          | 1145  | default |

    Scenario: Editing an extension with an exten outside of context range
        Given I have the following extensions:
          | exten | context |
          | 1453  | default |
        When I update the extension with exten "1453@default" using the following parameters:
          | exten |
          | 9999  |
      Then I get a response with status "400"
      Then I get an error message "Invalid parameters: exten 9999 not inside range of context default"

    Scenario: Editing the context of a extension
        Given I have no extension with exten "1833@toto"
        Given I have the following extensions:
          | exten | context |
          | 1833  | default |
        Given I have the following context:
          | name | numberbeg | numberend |
          | toto | 1000      | 1999      |
        When I update the extension with exten "1833@default" using the following parameters:
          | context |
          | toto    |
        Then I get a response with status "204"
        When I access the extension with exten "1833@toto"
        Then I have an extension with the following parameters:
          | exten | context |
          | 1833  | toto    |

    Scenario: Editing the extension with a context that doesn't exist
        Given I have the following extensions:
          | exten | context |
          | 1665  | default |
        When I update the extension with exten "1665@default" using the following parameters:
          | context             |
          | mysuperdupercontext |
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: context mysuperdupercontext does not exist"

    Scenario: Editing the exten, context of a extension
        Given I have no extension with exten "1996@patate"
        Given I have the following extensions:
          | exten | context |
          | 1292  | default |
        Given I have the following context:
          | name   | numberbeg | numberend |
          | patate | 1000      | 1999      |
        When I update the extension with exten "1292@default" using the following parameters:
          | exten | context |
          | 1996  | patate  |
        Then I get a response with status "204"
        When I access the extension with exten "1996@patate"
        Then I have an extension with the following parameters:
          | exten | context |
          | 1996  | patate  |

    Scenario: Editing a commented extension
        Given I have the following extensions:
          | exten | context | commented |
          | 1107  | default | true      |
        When I update the extension with exten "1107@default" using the following parameters:
          | commented |
          | false     |
        Then I get a response with status "204"
        When I access the extension with exten "1107@default"
        Then I have an extension with the following parameters:
          | exten | context | commented |
          | 1107  | default | false     |

    Scenario: Delete an extension that doesn't exist
        When I delete a fake extension
        Then I get a response with status "404"

    Scenario: Delete an extension
        Given I have the following extensions:
            | exten | context |
            | 1846  | default |
        When I delete extension with exten "1846@default"
        Then I get a response with status "204"
        Then the extension with exten "1846@default" no longer exists

    Scenario: Delete an extension associated to a line
        Given I have the following lines:
            | id     | context | protocol | device_slot |
            | 299568 | default | sip      | 1           |
        Given I have the following extensions:
            | exten | context |
            | 1226  | default |
        Given line "299568" is linked with extension "1226@default"
        When I delete extension with exten "1226@default"
        Then I get a response with status "400"
        Then I get an error message "Error while deleting Extension: extension still has a link"
