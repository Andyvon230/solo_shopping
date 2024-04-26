Feature: Cart Functionality

  Scenario: User is not logged in
    Given the user is not logged in
    When the cart function is called
    Then the response should be "User not logged in" with status code 403

  Scenario: User is logged in and has valid carts
    Given the user is logged in
    And the user has valid carts
    When the cart function is called
    Then the response should render the "carts/cart.html" template with the correct carts and total price

  Scenario: User is logged in and has invalid carts
    Given the user is logged in
    And the user has invalid carts
    When the cart function is called
    Then the response should render the "carts/cart.html" template with the correct carts and total price

  Scenario: Exception occurs during execution
    Given the user is logged in
    And the user has valid carts
    And an exception occurs during execution
    When the cart function is called
    Then the response should be an error message with status code 500