Feature: Order List
    As a user
    I want to view the order list
    So that I can manage orders

Scenario: View Order List
    Given I am logged in as an admin
    When I visit the order list page
    Then I should see the order list
    And the order list should not be empty