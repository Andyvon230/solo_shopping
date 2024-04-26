Feature: Home Page

  Scenario: Viewing the home page without search input
    Given I am on the home page
    Then I should see the merchandise list

  Scenario: Viewing the home page with search input
    Given I am on the home page
    And I enter "search_input" in the search field
    When I submit the search form
    Then I should see the search results