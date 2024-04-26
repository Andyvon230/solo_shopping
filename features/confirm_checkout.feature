Feature: Confirm Checkout
  Scenario: User is not authenticated
    Given the user is not authenticated
    When the user attempts to confirm checkout
    Then they should be redirected to the login page

  Scenario: Cart is empty
    Given the user is authenticated
    And the cart is empty
    When the user attempts to confirm checkout
    Then they should see an error message
    And they should be redirected to the cart page

  Scenario: Successful checkout
    Given the user is authenticated
    And the cart is not empty
    When the user confirms checkout
    Then their order should be placed successfully
    And they should be redirected to the success page

  Scenario: Error during checkout
    Given the user is authenticated
    And the cart is not empty
    When the checkout process encounters an error
    Then they should see an error message
    And they should be redirected to the cart page