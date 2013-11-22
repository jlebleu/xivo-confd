Feature: REST API Users

    Scenario: User list with no users
        Given I have no users
        When I ask for the list of users via RESTAPI
        Then I get an empty list

    Scenario: User list with one user
        Given there are users with infos:
          | firstname | lastname |
          | Clémence  | Dupond   |
        When I ask for the list of users via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname | userfield | callerid          |
          | Clémence  | Dupond   |           | "Clémence Dupond" |

    Scenario: User list with two users
        Given there are users with infos:
          | firstname | lastname |
          | Clémence  | Dupond   |
          | Louis     | Martin   |
        When I ask for the list of users via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname | userfield | callerid          |
          | Clémence  | Dupond   |           | "Clémence Dupond" |
          | Louis     | Martin   |           | "Louis Martin"    |

    Scenario: User list ordered by lastname, then firstname
        Given there are users with infos:
          | firstname | lastname |
          | Clémence  | Dupond   |
          | Louis     | Martin   |
          | Albert    | Dupond   |
          | Frédéric  | Martin   |
        When I ask for the list of users via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname | userfield | callerid          |
          | Albert    | Dupond   |           | "Albert Dupond"   |
          | Clémence  | Dupond   |           | "Clémence Dupond" |
          | Frédéric  | Martin   |           | "Frédéric Martin" |
          | Louis     | Martin   |           | "Louis Martin"    |

    Scenario: User search with no users
        Given I have no users
        When I search for the user "Bob" via RESTAPI
        Then I get an empty list

    Scenario: User search with an empty filter
        Given there are users with infos:
          | firstname | lastname |
          | George    | Lucas    |
        When I search for the user "" via RESTAPI
        Then I get a list with the following users via RESTAPI:
         | firstname | lastname | callerid       |
         | George    | Lucas    | "George Lucas" |

    Scenario: User search with a filter that returns nothing
        Given there are users with infos:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "bob" via RESTAPI
        Then I get an empty list
        When I search for the user "rei" via RESTAPI
        Then I get an empty list

    Scenario: User search using the firstname
        Given there are users with infos:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "and" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "reï" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "andou" via RESTAPI
        Then I get an empty list

    Scenario: User search using the lastname
        Given there are users with infos:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "lie" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "bél" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "belou" via RESTAPI
        Then I get an empty list

    Scenario: User search using the firstname and lastname
        Given there are users with infos:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "andreï" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "bélier" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "reï bél" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
        When I search for the user "rei bel" via RESTAPI
        Then I get an empty list

    Scenario: User search with 2 users
        Given there are users with infos:
          | firstname | lastname |
          | Remy      | Licorne  |
          | Andreï    | Bélier   |
        When I search for the user "re" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Andreï    | Bélier   |
          | Remy      | Licorne  |
        When I search for the user "lic" via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname |
          | Remy      | Licorne  |

    Scenario: Getting a user that doesn't exist
        Given I have no users
        When I ask for the user with id "1" via RESTAPI
        Then I get a response with status "404"

    Scenario: Getting a user that exists
        Given there are users with infos:
          | id | firstname | lastname |
          | 1  | Irène     | Dupont   |
        When I ask for the user with id "1" via RESTAPI
        Then I get a response with status "200"
        'Then I get a user with the following parameters via RESTAPI:
          | id | firstname | lastname | userfield |
          | 1  | Irène     | Dupont   |           |

    Scenario: Creating an empty user
        Given I have no users
        When I create an empty user via RESTAPI
        Then I get a response with status "400"
        Then I get an error message "Missing parameters: firstname"

    Scenario: Creating a user with paramters that don't exist
        Given I have no users
        When I create users with the following parameters via RESTAPI:
          | unexisting_field |
          | unexisting_value |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: unexisting_field"

    Scenario: Creating a user with a firstname and parameters that don't exist
        Given I have no users
        When I create users with the following parameters via RESTAPI:
          | firstname | unexisting_field |
          | Joe       | unexisting_value |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: unexisting_field"

    Scenario: Creating a user with a firstname
        Given I have no users
        When I create users with the following parameters via RESTAPI:
          | firstname |
          | Irène     |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "users" resource
        Then I get a response with a link to the "users" resource
        Then the created user has the following parameters via RESTAPI:
         | firstname | lastname | userfield | callerid |
         | Irène     |          |           | "Irène " |

    Scenario: Creating two users with the same firstname
        Given I have no users
        When I create users with the following parameters via RESTAPI:
          | firstname |
          | Lord      |
          | Lord      |
        When I ask for the list of users via RESTAPI
        Then I get a list with the following users via RESTAPI:
          | firstname | lastname | userfield | callerid |
          | Lord      |          |           | "Lord "  |
          | Lord      |          |           | "Lord "  |

    Scenario: Creating a user with multiple fields
        Given I have no users
        When I create users with the following parameters via RESTAPI:
          | firstname | lastname | description                 | userfield  | musiconhold | preprocess_subroutine |
          | Irène     | Dupont   | accented description: éà@'; | customdata | folksong    | my_subroutine         |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "users" resource
        Then I get a response with a link to the "users" resource
        Then the created user has the following parameters via RESTAPI:
          | firstname | lastname | description                 | userfield  | callerid       | musiconhold | preprocess_subroutine |
          | Irène     | Dupont   | accented description: éà@'; | customdata | "Irène Dupont" | folksong    | my_subroutine         |

    Scenario: Editing a user that doesn't exist
        Given I have no users
        When I update the user with id "1" using the following parameters via RESTAPI:
          | firstname |
          | Bob       |
        Then I get a response with status "404"

    Scenario: Editing a user with parameters that don't exist
        Given there are users with infos:
          |     id | firstname | lastname |
          | 995435 | Clémence  | Dupond   |
        When I update the user with id "995435" using the following parameters via RESTAPI:
          | unexisting_field |
          | unexisting value |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: unexisting_field"

    Scenario: Editing the firstname of a user
        Given there are users with infos:
          |     id | firstname | lastname |
          | 995414 | Clémence  | Dupond   |
        When I update the user with id "995414" using the following parameters via RESTAPI:
          | firstname |
          | Brézé     |
        Then I get a response with status "204"
        When I ask for the user with id "995414" via RESTAPI
        'Then I get a user with the following parameters via RESTAPI:
          |     id | firstname | lastname | userfield | callerid       |
          | 995414 | Brézé     | Dupond   |           | "Brézé Dupond" |

    Scenario: Editing the lastname of a user
        Given there are users with infos:
          |     id | firstname | lastname |
          | 924465 | Clémence  | Dupond   |
        When I update the user with id "924465" using the following parameters via RESTAPI:
          | lastname      |
          | Argentine     |
        Then I get a response with status "204"
        When I ask for the user with id "924465" via RESTAPI
        'Then I get a user with the following parameters via RESTAPI:
          |     id | firstname | lastname  | userfield | callerid             |
          | 924465 | Clémence  | Argentine |           | "Clémence Argentine" |

    Scenario: Editing multiple fields of a user
        Given there are users with infos:
          |     id | firstname | lastname |
          | 113549 | Clémence  | Dupond   |
        When I update the user with id "113549" using the following parameters via RESTAPI:
          | firstname | lastname  | userfield  | musiconhold | preprocess_subroutine |
          | Claude    | Argentine | customdata | country     | my_subroutine         |
        Then I get a response with status "204"
        When I ask for the user with id "113549" via RESTAPI
        'Then I get a user with the following parameters via RESTAPI:
          | id     | firstname | lastname  | userfield  | callerid           | musiconhold | preprocess_subroutine |
          | 113549 | Claude    | Argentine | customdata | "Claude Argentine" | country     | my_subroutine         |

    Scenario: Editing a user associated with a voicemail
        Given there are users with infos:
            |id      | firstname | lastname  | number | context | protocol | voicemail_name     | voicemail_number |
            | 456903 | Francois  | Andouille | 1100   | default | sip      | Francois Andouille | 1100             |
        When I update the user with id "456903" using the following parameters via RESTAPI:
            | firstname | lastname |
            | Pizza     | Poulet   |
        Then I get a response with status "204"
        When I send a request for the voicemail "1100@default", using its id
        Then I have the following voicemails via RESTAPI:
            | name         | number |
            | Pizza Poulet | 1100   |

    Scenario: Deleting a user that doesn't exist
        Given I have no users
        When I delete the user with id "1" via RESTAPI
        Then I get a response with status "404"

    Scenario: Deleting a user
        Given there are users with infos:
          |     id | firstname | lastname |
          | 955135 | Clémence  | Dupond   |
        When I delete the user with id "955135" via RESTAPI
        Then I get a response with status "204"
        Then the user with id "955135" no longer exists via RESTAPI

    Scenario: Deleting a user still has a link
        Given there are users with infos:
            |     id | firstname | lastname |
            | 956541 | Clémence  | Dupond   |
        Given I only have the following lines:
            |     id | context | protocol | device_slot |
            | 546216 | default | sip      |           1 |
        Given I only have the following extensions:
            |     id | context | exten | type | typeval |
            | 951654 | default |  1000 | user |  956541 |
        When I create the following links:
            | user_id | line_id | extension_id | main_line |
            |  956541 |  546216 |       951654 | True      |

        When I delete the user with id "956541" via RESTAPI
        Then I get a response with status "400"
        Then I get an error message "Error while deleting User: user still has a link"

    Scenario: List the links associated to a user with no links
        Given there are users with infos:
            |     id | firstname | lastname |
            | 989465 | Francisco | Montoya  |
        When I get the lines associated to user "989465" via RESTAPI
        Then I get an empty list

    Scenario: List the links associated to a user
        Given there are users with infos:
            |     id | firstname | lastname |
            | 994775 | Jacen     | Solo     |
            | 112348 | Anakin    | Solo     |
        Given I only have the following lines:
            |     id | context | protocol | device_slot |
            | 135498 | default | sip      |           1 |
            | 133364 | default | sip      |           1 |
        Given I only have the following extensions:
            |     id | context | exten | type | typeval |
            | 995135 | default |  1001 | user |  994775 |
            | 132468 | default |  1002 | user |  112348 |
        Given the following users, lines, extensions are linked:
            | user_id | line_id | extension_id | main_line |
            |  994775 |  135498 |       995135 | True      |
            |  112348 |  133364 |       132468 | True      |

        When I get the lines associated to user "994775" via RESTAPI
        Then I get a response with status "200"
        Then I get the user_links with the following parameters:
            | user_id | line_id | extension_id |
            |  994775 |  135498 |       995135 |
        Then I do not get the user_links with the following parameters:
            | user_id | line_id | extension_id |
            |  112348 |  133364 |       132468 |
