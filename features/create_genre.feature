Feature: Create genre
  In order to calificate a book I searched for, 
  As a user, 
  I want to create a genre given the book’s name if the genre doesn’t exist already.

  
Background: There is a registered user
    Given Exists a user "testuser" with password "testpassword"

Scenario: Register just restaurant name
    Given I login as user "testuser" with password "testpassword"
    When I create genre
      | name        |
      | Genre12345  |
    Then There is 1 genre in my genre list
      | name        |
      | The Tavern  |