Feature: Modify Review
    In order to keep my reviews updates for a book, 
    As a user, 
    I want to add more content or modify it.


Background: There is a registered user
    Given Exists a user "testuser" with password "testpassword"
    And A book "BookA" by author "AuthA"
    And A review for book "BookA"
      | title   | score | text      |
      | WOW     | 8     | Good book |

Scenario: Create review
    Given I login as user "testuser" with password "testpassword"
    When I modify review "WOW" for book "BookA"
      | title   | score | text      |
      | WOW     | 0     | Good book |
    Then There are 1 reviews in my review list
    And The new score for review "WOW" is 0