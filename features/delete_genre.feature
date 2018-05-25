Feature: Delete Genre
    In order to edit a genre I made, 
    As a user, 
    I want to invalid it.

Background: There is a registered user
    Given Exists a user "testuser" with password "testpassword"
    And I create genre
      | name        |
      | Genre12345  | 

Scenario: Delete genre
    Given I login as user "testuser" with password "testpassword"
    When I delete genre
      | name        |
      | Genre12345  |
    Then There are 0 genres in my genre list