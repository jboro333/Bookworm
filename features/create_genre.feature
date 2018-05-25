Feature: Create genre
  In order to calificate a book I searched for, 
  As a user, 
  I want to create a genre given the book’s name if the genre doesn’t exist already.

  
Background: There is a registered user
    Given Exists a user "testuser" with password "testpassword"

Scenario: Create genre
    Given I login as user "testuser" with password "testpassword"
    When I create genre
      | name        |
      | Genre12345  |
    Then There are 1 genres in my genre list